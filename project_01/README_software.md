# StikE — Software README

StikE is a pocketable, dual-display task tracker built on the ESP32-S3. This document covers the software: architecture, build setup, usage, and code organization. For hardware — PCB design, schematics, and BOM — see [`README_hardware.md`](./README_hardware.md). For the full project writeup, see the [Hackster.io page](https://www.hackster.io/bm150/stike-note-e0d2a9).

---

## Repository Structure

```
stike/
├── src/
│   ├── main.cpp          # Entry point, FreeRTOS setup, state machine, persistence
│   ├── display_mgr.cpp   # TFT + ePaper rendering pipeline
│   ├── keyboard_mgr.cpp  # I2C keyboard driver (M5Stack CardKB)
│   └── systems_test.cpp  # Hardware diagnostic suite (conditional)
├── include/
│   ├── state_types.h     # Core enums, structs, and constants
│   ├── display_mgr.h     # DisplayManager class definition
│   ├── keyboard_mgr.h    # KeyboardManager class definition
│   ├── power_mgr.h       # Low-power mode flag and setter
│   ├── pins.h            # All GPIO pin mappings
│   ├── icons.h           # PROGMEM icon bitmaps
│   └── systems_test.h    # SystemsTest class (conditional)
├── esp32-s3-devkitc-1-n16r8v.json   # Custom PlatformIO board definition
└── platformio.ini
```

---

## Architecture Overview

The firmware runs on the Arduino framework via PlatformIO, with FreeRTOS managing dual-core task scheduling. The overall design is an **event-driven state machine**: hardware input is polled asynchronously on one core, translated into events, and processed by the main application loop on the other.

### Dual-Core Split

```
┌─────────────────────────────┐     ┌──────────────────────────────────────┐
│          Core 0             │     │              Core 1                  │
│                             │     │                                      │
│  keyboardTask()             │     │  loop()                              │
│  └─ KeyboardManager.poll()  │     │  └─ xQueueReceive(eventQueue)        │
│     └─ push SystemEvent ────┼────►│     └─ state handler dispatch        │
│        to eventQueue        │     │        └─ DisplayManager.render()    │
└─────────────────────────────┘     └──────────────────────────────────────┘
```

**Core 0** runs a single dedicated FreeRTOS task. It polls the M5Stack CardKB over I2C at address `0x5F`, translates raw bytes into `SystemEvent` structs, and pushes them onto a shared FreeRTOS queue. It does nothing else — no display writes, no state management.

**Core 1** runs the main Arduino `loop()`. It blocks on the event queue and, when an event arrives, hands it to whichever state handler is currently active. After processing, it calls `DisplayManager` to redraw the TFT. The ePaper display is updated asynchronously on sleep cycle wakes, separate from this loop.

The queue between the cores means neither side blocks the other. SPI display writes are slow enough that if keyboard polling had to share time with them, you'd feel the latency. Keeping them apart eliminates that entirely.

### State Machine

`currentState` is a global `SystemState` enum. The main loop dispatches every incoming event to the handler for the current state, which may transition to a new state by writing to `currentState`. The next loop tick picks up in the new context.

| State | Description |
|---|---|
| `STATE_UI_LIST` | Task list view — the default on wake |
| `STATE_UI_CALENDAR` | Calendar view (month, week, or day) |
| `STATE_UI_ADD_TASK` | Text input for adding a new task |
| `STATE_UI_EDIT_TASK` | Text input for editing an existing task |
| `STATE_UI_QUICK_ADD` | Abbreviated task add flow |
| `STATE_UI_SETTINGS` | Settings screen |
| `STATE_UI_POMODORO` | Pomodoro timer |
| `STATE_SLEEP` | Deep sleep — TFT off, ePaper cycling |
| `STATE_EPAPER_UPDATE` | Triggered to push new content to the ePaper |

### Key Data Structures (`state_types.h`)

**`TaskItem`** — a to-do entry. Fields: `title`, `completed`, creation timestamp, completion date, optional due date.

**`CalendarEvent`** — a scheduled event. Fields: `title`, `notes`, `location`, date/time (year, month, day, hour, minute), duration, optional `linkedTaskId` to associate it with a task.

**`SystemEvent`** — the unit that travels through the FreeRTOS queue. Contains a `SystemEventType` (e.g., `EVENT_NAV_UP`, `EVENT_SELECT`, `EVENT_TYPE_CHAR`, `SLEEP_REQ`) and an integer `param` (used to carry the character code for typing events).

**`EpaperItem` / `EpaperViewItem`** — wrappers used to pack tasks and events into discrete screens for the ePaper display. Each `EpaperViewItem` holds up to `ITEMS_PER_EPAPER_SCREEN = 6` items. Up to `EPAPER_VIEW_COUNT = 10` screens are prepared at a time.

### System Constants

| Constant | Value | Purpose |
|---|---|---|
| `MAX_TASKS` | 20 | Fixed task array size |
| `MAX_CALENDAR_EVENTS` | 50 | Fixed calendar array size |
| `ITEMS_PER_EPAPER_SCREEN` | 6 | Items shown per ePaper view |
| `EPAPER_VIEW_COUNT` | 10 | Maximum ePaper screens prepared |
| `SLEEP_DURATION_US` | 10,000,000 | Sleep cycle length (10 seconds) |
| `INPUT_BUFFER_SIZE` | 32 | Max characters in a text input buffer |

---

## Modules

### `main.cpp` — Entry Point and State Machine

`setup()` runs first: it starts serial, initializes NVS and loads saved data, brings up the display and keyboard managers in the correct order (ePaper first, then TFT — see note below), and creates the FreeRTOS event queue and tasks.

`loop()` is the Core 1 event processor. It blocks on the queue and dispatches to state-specific handler functions. State handlers for each UI mode live here — task list navigation, calendar browsing, text input for add/edit flows, pomodoro logic, and settings.

Persistence is handled inline in `main.cpp`: whenever tasks or calendar events are modified, the relevant array is serialized to NVS via `Preferences` as a binary blob. On boot, those blobs are read back and the arrays are restored in place. No dynamic allocation is used anywhere in the persistence path.

> **Initialization order note:** The ePaper display must be initialized and hibernated before the TFT is initialized. Both displays share electrical infrastructure, and bringing them up simultaneously causes SPI bus contention that leaves both in an undefined state. The sequencing in `setup()` is deliberate and should not be changed.

### `display_mgr.cpp` — Display Rendering

`DisplayManager` handles both screens behind a single interface.

For the **TFT**, rendering uses a software sprite from the `TFT_eSPI` library. All drawing calls go to the sprite buffer in RAM. When a frame is ready, the entire buffer is pushed to the hardware in one operation. This prevents the incremental tearing that would otherwise be visible on a dynamic UI over a slow SPI bus.

For the **ePaper**, the display manager filters the active task list and upcoming calendar events into `EpaperViewItem` arrays, then determines whether a partial or full refresh is needed. Full refreshes take several seconds and visibly cycle the display; partial updates are faster but accumulate image retention over multiple cycles. The manager balances these based on update frequency.

`DisplayManager` also exposes `getDaysInMonth()` as a static utility used by the calendar rendering logic.

### `keyboard_mgr.cpp` — Keyboard Driver

`KeyboardManager` wraps the M5Stack CardKB over I2C. `init()` sets up the bus on pins `SDA=18`, `SCL=21` at the configured clock speed. `getKeyPress()` reads a raw byte from address `0x5F` and translates it to a character.

The CardKB maps `Fn + key` combinations to hardcoded hex values based on physical key position rather than standard ASCII offsets. These mappings are handled explicitly in `getKeyPress()`. `scanBus()` is available as a debug utility to enumerate I2C devices on the bus.

### `power_mgr.h` — Low-Power Mode

A global `isLowPowerMode` flag controls whether the system is in a battery-conserving state. When enabled via `setLowPowerMode(true)`, the CPU frequency is reduced and FreeRTOS task polling delays are increased. This is toggled from the Settings screen.

### `systems_test.cpp` — Diagnostic Suite

The `SystemsTest` class is compiled only when `STike_SYSTEM_TEST` is defined. It provides a serial command interface (`handleSerialInput`) and physical keyboard test mode (`handleKeyPress`) for hardware validation. Test sub-modes include TFT color pattern rendering, ePaper refresh testing, sleep cycle testing, and keyboard matrix verification. All output goes to the serial console.

---

## Getting Started

### Prerequisites

- Python 3
- PlatformIO Core CLI

```bash
python3 -m pip install -U platformio
```

### Board Configuration

The ESP32-S3 DevKitC-1 N16R8 variant requires a custom board definition that is not included in PlatformIO's default registry. Copy it once:

```bash
mkdir -p ~/.platformio/boards
cp esp32-s3-devkitc-1-n16r8v.json ~/.platformio/boards/
```

### Compile

```bash
python3 -m platformio run -e esp32-s3-devkitc-1-n16r8v
```

### Upload

With the device connected over USB-C:

```bash
python3 -m platformio run -t upload -e esp32-s3-devkitc-1-n16r8v
```

If the upload fails to connect, hold the `BOOT` button on the ESP32 module while initiating the upload, then release once the upload begins.

### Testing Without Hardware

Pure C++ logic (data structures, state transitions, NVS serialization logic) can be compiled and tested with `g++` using mock header files, without any hardware dependencies. This is useful for validating state machine logic in isolation.

---

## Using the Device

### Power On

On boot, the device initializes both buses, loads saved tasks and calendar events from NVS, and opens in the Task List view (`STATE_UI_LIST`).

### Navigation

| Key | Action |
|---|---|
| Arrow Up / Down | Move selection up or down |
| Arrow Left / Right | Navigate between views or columns |
| Enter | Select / confirm |
| Esc | Cancel / go back |
| Backspace | Delete character (in text input) |

### Key Shortcuts (from Task List)

| Key | Action |
|---|---|
| `a` | Add new task |
| `c` | Open calendar |
| `p` | Start pomodoro timer |
| `s` | Open settings |

### Calendar

From the calendar view, use Left/Right to move between month, week, and day perspectives. Navigate to a day and press Enter to view or add events for that day.

### Task Filters

In the task list, cycle through `ACTIVE`, `COMPLETED`, and `BOTH` filters using the designated key. The filter state is preserved across sleep cycles.

### Sleep and Wake

The device enters sleep automatically after a period of inactivity. The TFT backlight cuts and the ESP32 enters deep sleep. The ePaper display continues to show the last pushed task/event list.

To wake: press any key on the CardKB, or open the device lid (the Hall effect switch on the hinge sends a wake pulse to GPIO 14). On wake, the device resumes in `STATE_UI_LIST` with all data intact.

---

## System Test Mode

To enable the diagnostic suite, define `STike_SYSTEM_TEST` in your build environment (add `-D STike_SYSTEM_TEST` to `build_flags` in `platformio.ini`). On boot, the device enters test mode instead of the normal application flow.

Available tests via the serial monitor:

| Command | Test |
|---|---|
| `t` | TFT color bar pattern |
| `e` | ePaper test pattern / refresh cycle |
| `s` | Sleep / wake cycle |
| `k` | Keyboard matrix — physical key press logging |
| `i` | I2C bus scan |

All test output is logged to the serial console at the configured baud rate.

---

## Dependencies

All library dependencies are managed through PlatformIO and defined in `platformio.ini`.

| Library | Purpose |
|---|---|
| `TFT_eSPI` | ST7735S TFT display driver and sprite rendering |
| `GxEPD2` | GDEQ0213B74 ePaper display driver |
| `Wire` | Arduino I2C library (keyboard bus) |
| `Preferences` | ESP32 NVS abstraction (persistence) |
| `FreeRTOS` | Included with ESP32 Arduino core |
| `esp_sleep` | ESP32 deep sleep and wake configuration |

---
## Acknowledgements
I would like to formally acknowledge the aid of LLMs in the construction, but particularly the robust documentation of this project. To maintain the integrity of my education, LLMs played an auxilliary, rather than principal role in construction. Models utilized were Gemini 3 Flash, Gemini 3.1 and 3.2 Pro.

---

## Links

- Hardware README: [`README_hardware.md`](./README_hardware.md)
- Hackster.io: [Project Page](https://www.hackster.io/bm150/stike-note-e0d2a9)
- PCB Files: [`project_02/hardware/`](./project_02/hardware/)

---