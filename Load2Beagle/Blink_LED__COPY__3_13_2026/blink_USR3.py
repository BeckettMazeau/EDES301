"""
---------------------------------------------------------------------------

Blink LED (For PocketBeagle Rev A2B)

---------------------------------------------------------------------------

Blinks the USR3 LED onboard a PocketBeagle 1 at 5Hz.

This module utilizes the Adafruit_BBIO library to control the GPIO pins.
It sets up the USR3 LED as an output and toggles its state in a time-limited
loop to create a 5Hz blinking effect.

---------------------------------------------------------------------------

Authors: Beckett Lyons Mazeau (beckett.mazeau@rice.edu)

Copyright 2026, Beckett Lyons Mazeau

License:
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

---------------------------------------------------------------------------

"""

import Adafruit_BBIO as GPIO
import time

#: bool: Global flag tracking the current illumination state of the USR3 LED.
LEDSTATE = False


def toggle_LED():
    """Toggles the state of the USR3 LED.

    This function accesses the global `LEDSTATE` variable, inverts its boolean
    value, and writes the corresponding HIGH or LOW signal to the USR3 GPIO pin.
    With a 0.1-second sleep interval between calls, this creates a full cycle
    every 0.2 seconds, resulting in a 5Hz frequency.
    """
    global LEDSTATE
    LEDSTATE = not LEDSTATE
    if LEDSTATE:
        # Output HIGH to turn the LED on
        GPIO.output("USR3", GPIO.HIGH)
    else:
        # Output LOW to turn the LED off
        GPIO.output("USR3", GPIO.LOW)


if __name__ == "__main__":
    # Initialize the USR3 pin as a digital output
    GPIO.setup("USR3", GPIO.OUT)

    # Record the start time in seconds since the epoch
    startTime = time.time()

    # Continue toggling for 20,000 seconds
    while time.time() - startTime < 20:
        toggle_LED()
        # Pause execution for 0.1 seconds to serve as the half-period
        time.sleep(0.1)
