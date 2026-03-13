# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------

Simple Calculator

--------------------------------------------------------------------------

Simple calculator that will
  - Take in an operator from the user
  - Take in two numbers from the user
  - Perform the mathematical operation and display the result
  - Repeat until the user enters an exit command

Operations:
  - "+"  / "add"      : addition
  - "-"  / "sub"      : subtraction
  - "*"  / "multiply" : multiplication
  - "/"  / "div"      : division
  - "%"  / "mod"      : modulus
  - "^"  / "pow"      : exponentiation
  - ">>" / "rshift"   : bitwise right shift (integers only)
  - "<<" / "lshift"   : bitwise left shift  (integers only)

  Note: Each operation also accepts a variety of verbose aliases
  (e.g. "addition", "subtraction", "right shift", "left shift", etc.)

Exit commands:
  - "exit", "stop", "end" --> Program exits cleanly

Error conditions:
  - Invalid operator        --> Re-prompts until valid input is received
  - Invalid number          --> Re-prompts until valid input is received
  - Float passed to shift   --> Operands are cast to integer with warning

--------------------------------------------------------------------------

License:   
Copyright 2026 - <Beckett Mazeau>

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, 
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

"""

# NOTE - Add import statements to allow access to Python library functions
# NOTE - Hint:  Look at  https://docs.python.org/3/library/operator.html
import operator  # Provides standard arithmetic and bitwise operator functions
import re  # Provides regular expression matching for input sanitization
from operator import truediv  # Explicit import of truediv for float division support

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

# NOTE - No constants are needed for this example 

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# NOTE - Global variable to map an operator string (e.g. "+") to 
# NOTE - the appropriate function.

#: dict: Maps user-entered operator strings (symbols and words) to their
#: corresponding ``operator`` module functions, plus sentinel strings for
#: program exit commands.  Supports symbolic (``"+"``, ``">>"``) and
#: verbose (``"addition"``, ``"right shift"``) input aliases.
operators = {
    "+" : operator.add,
    "-" : operator.sub,
    "*" : operator.mul,
    "/" : operator.truediv,
    "add" : operator.add,
    "addition" : operator.add,
    "sub" : operator.sub,
    "subtract" : operator.sub,
    "subtraction" : operator.sub,
    "multiply" : operator.mul,
    "multiplication" : operator.mul,
    "div" : operator.truediv,
    "divide" : operator.truediv,
    "division" : operator.truediv,
    "right shift" : operator.rshift,
    "rshift": operator.rshift,
    "right-shift": operator.rshift,
    "shift right": operator.rshift,
    ">>": operator.rshift,
    "signed right shift": operator.rshift,
    "left shift": operator.lshift,
    "lshift": operator.lshift,
    "left-shift": operator.lshift,
    "shift left": operator.lshift,
    "<<": operator.lshift,
    "zero fill left shift": operator.lshift,
    "mod": operator.mod,
    "modulus": operator.mod,
    "modulo": operator.mod,
    "%": operator.mod,
    "^": operator.pow,
    "**": operator.pow,
    "pow": operator.pow,
    "power": operator.pow,
    "raise": operator.pow,
    "raised": operator.pow,
    "exponent": operator.pow,
    "exponentiation": operator.pow,

    "stop":"exit",
    "exit":"exit",
    "end": "exit"
}

#: dict: Reverse-lookup table mapping each ``operator`` module function back
#: to its canonical symbol string, used when formatting the result output line.
ops_to_symbols = {
    operator.add: "+",
    operator.sub: "-",
    operator.mul: "*",
    operator.truediv: "/",
    operator.lshift : "<<",
    operator.mod: "%",
    operator.pow: "^",
    operator.rshift : ">>"
}



# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------

def get_user_input():
    """Prompt the user for an operator and two operands, with input validation.

    Requests the desired operation first, then each operand in turn.
    Each prompt loops until valid input is received.  Digit characters are
    stripped from the operator string and non-numeric characters are stripped
    from each number string before validation.

    The function first attempts to use ``raw_input`` (Python 2).  If a
    ``NameError`` is raised (Python 3 environment), it falls back to the
    built-in ``input`` function.

    Returns:
        tuple: A three-element tuple in one of two forms:

            * ``(str, float, float)`` -- A validated operator key from
              :data:`operators`, followed by the two numeric operands.
            * ``("exit", None, None)`` -- Returned when the user enters an
              exit command (``"exit"``, ``"stop"``, or ``"end"``).
    """
    # NOTE - Use "try"/"except" statements to allow code to handle errors gracefully.

    # Flags to control each input-validation loop; True means still waiting
    novalid_input1 = True
    novalid_input2 = True
    novalid_input3 = True

    # Initialize inputs to empty strings so they are defined before use
    operation_input = ""
    number1_input = ""
    number2_input = ""

    try:
        # --- Python 2 path: raw_input is available ---

        while novalid_input1:
            # Prompt the user to choose an operation
            operation_input = raw_input("Please enter the operation to be performed.\n"
                               "Available operations: \n"+
                               "Addition: +\n"
                               "Subtraction: -\n"
                               "Multiplication: *\n"
                               "Division: /\n"
                               "Modulus: %\n"
                               "Right Shift: >>\n"
                               "Left Shift: <<\n"
                               "Exit Program: Exit")

            # Normalize: strip digits and surrounding whitespace, convert to lowercase
            operation_input = re.sub(r'\d+', '', operation_input.strip().lower())

            # Reject empty or unrecognized operator strings and re-prompt
            if (operation_input not in operators) or (operation_input == "") or operation_input == None:
                print("Invalid Input, please try again.\n"
                      "Reference the attached table for valid inputs.\n")
                continue

            # Return sentinel tuple when user requests program exit
            if operators[operation_input] == "exit":
                return("exit",None,None)

            novalid_input1 = False  # Valid operator received; exit the loop

        while (novalid_input2):
            try:
                # Strip any non-numeric characters then cast to float
                number1_input = float(re.sub(r'[^0-9,.]', '', raw_input("Please enter the first number in the chosen operation.\n: ")))
            except:
                print("Invalid Input, please try again.\n")
                continue

            # Guard against empty string slipping through after regex stripping
            if number1_input == "" or number1_input == None:
                print("Invalid Input, please try again.\n")
                continue

            novalid_input2 = False  # Valid first operand received; exit the loop

        while (novalid_input3):
            try:
                # Strip any non-numeric characters then cast to float
                number2_input = float(re.sub(r'[^0-9,.]', '', raw_input("Please enter the second number in the chosen operation.\n: ")))
            except:
                print("Invalid Input, please try again.\n")
                continue

            # Guard against empty string slipping through after regex stripping
            if number2_input == "" or number2_input == None:
                print("Invalid Input, please try again.\n")
                continue

            novalid_input3 = False  # Valid second operand received; exit the loop

        return(operation_input, number1_input, number2_input)

    except NameError:
        # --- Python 3 fallback: raw_input does not exist, use input() instead ---

        # Prompt for operation using Python 3 built-in input()
        operation_input = input("Please enter the operation to be performed.\n"
                                "Available operations: \n" +
                                "Addition: +\n"
                                "Subtraction: -\n"
                                "Multiplication: *\n"
                                "Division: /\n"
                                "Modulus: %\n"
                                "Right Shift: >>\n"
                                "Left Shift: <<\n"
                                "Exit Program: Exit")

        # Normalize: strip digits and surrounding whitespace, convert to lowercase
        operation_input = re.sub(r'\d+', '', operation_input.strip().lower())

        # Reject empty or unrecognized operator strings and re-prompt
        if (operation_input not in operators) or (operation_input == "") or operation_input == None:
            print("Invalid Input, please try again.\n"
                  "Reference the attached table for valid inputs.\n")
            continue

        # Return sentinel tuple when user requests program exit
        if operators[operation_input] == "exit":
            return ("exit", None, None)

        novalid_input1 = False  # Valid operator received; exit the loop

    while (novalid_input2):
        try:
            # Strip any non-numeric characters then cast to float
            number1_input = float(
                re.sub(r'[^0-9,.]', '', input("Please enter the first number in the chosen operation.\n: ")))
        except:
            print("Invalid Input, please try again.\n")
            continue

        # Guard against empty string slipping through after regex stripping
        if number1_input == "" or number1_input == None:
            print("Invalid Input, please try again.\n")
            continue

        novalid_input2 = False  # Valid first operand received; exit the loop

    while (novalid_input3):
        try:
            # Strip any non-numeric characters then cast to float
            number2_input = float(
                re.sub(r'[^0-9,.]', '', input("Please enter the second number in the chosen operation.\n: ")))
        except:
            print("Invalid Input, please try again.\n")
            continue

        # Guard against empty string slipping through after regex stripping
        if number2_input == "" or number2_input == None:
            print("Invalid Input, please try again.\n")
            continue

        novalid_input3 = False  # Valid second operand received; exit the loop

    return (operation_input, number1_input, number2_input)

# End def



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

# NOTE - The python variable "__name__" is provided by the language and can 
# NOTE - be used to determine how the file is being executed.  For example,
# NOTE - if the program is being executed on the command line:
# NOTE -   python3 simple_calc.py
# NOTE - then the "__name__" will be the string:  "__main__".  If the file 
# NOTE - is being imported into another python file:
# NOTE -   import simple_calc
# NOTE - the the "__name__" will be the module name, i.e. the string "simple_calc"

if __name__ == "__main__":
    run = True  # Control flag for the main REPL loop

    while run:
        # Collect and validate operator and operands from the user
        operator_input, number1_input, number2_input = get_user_input()

        op = ""  # Placeholder; op_symbol (below) carries the display symbol

        # Exit the loop cleanly if the user entered an exit command
        if operators[operator_input] == "exit":
            run = False
            print("Exiting...")
            break

        # Look up the display symbol (e.g. "+", ">>") for the chosen operation
        op_symbol = ops_to_symbols[operators[operator_input]]

        # Initialize working variables for the operands and result
        value = 0
        num1 = 0
        num2 = 0

        if op_symbol == ">>" or op_symbol == "<<":
            # Bitwise shift requires integer operands; attempt explicit cast
            try:
                num1 = int(number1_input)
                num2 = int(number2_input)
            except:
                print("An unexpected error occurred. Please try again.\n"
                      "Note: The selected operation does not support floats.")
                continue

            # Warn the user if either operand was implicitly truncated to int
            if (not float.is_integer(number1_input)) and (not float.is_integer(number2_input)):
                print("One or more input numbers are a non-integer.\n"
                      "Non-integers are not supported for this operation.\n"
                      "Casting to integer.")

        else:
            # All other operations work directly on the float values
            num1 = number1_input
            num2 = number2_input

        # Perform the selected operation and display the result to 5 decimal places
        value = operators[operator_input](num1, num2)
        print(f"\n\nOutput:\n {number1_input} {op_symbol} {number2_input} = {value:.5f}\n")
