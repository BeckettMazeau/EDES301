# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------

Simple Calculator

--------------------------------------------------------------------------

Simple calculator that will
  - Take in two numbers from the user
  - Take in an operator from the user
  - Perform the mathematical operation and provide the number to the user
  - Repeat

Operations:
  - "+" : addition
  - "-" : subtraction
  - "*" : multiplication
  - "/" : division

Error conditions:
  - Invalid operator --> Program should exit
  - Invalid number   --> Program should exit

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
import operator
import re
from operator import truediv

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

# NOTE - No constants are needed for this example 

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# NOTE - Global variable to map an operator string (e.g. "+") to 
# NOTE - the appropriate function.
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
    """ Get input from the user.
        Returns tuple:  (number, number, function) or 
                        (None, None, None) if inputs invalid
    """
    # NOTE - Use "try"/"except" statements to allow code to handle errors gracefully.
    novalid_input1 = True
    novalid_input2 = True
    novalid_input3 = True
    operation_input = ""
    number1_input = ""
    number2_input = ""
    try:
        while novalid_input1:
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
            operation_input = re.sub(r'\d+', '', operation_input.strip().lower())
            if (operation_input not in operators) or (operation_input == "") or operation_input == None:
                print("Invalid Input, please try again.\n"
                      "Reference the attached table for valid inputs.\n")
                continue
            if operators[operation_input] == "exit":
                return("exit",None,None)
            novalid_input1 = False
        while (novalid_input2):
            try:
                number1_input = float(re.sub(r'[^0-9,.]', '', raw_input("Please enter the first number in the chosen operation.\n: ")))
            except:
                print("Invalid Input, please try again.\n")
                continue
            if number1_input == "" or number1_input == None:
                print("Invalid Input, please try again.\n")
                continue
            novalid_input2 = False
        while (novalid_input3):
            try:
                number2_input = float(re.sub(r'[^0-9,.]', '', raw_input("Please enter the second number in the chosen operation.\n: ")))
            except:
                print("Invalid Input, please try again.\n")
                continue
            if number2_input == "" or number2_input == None:
                print("Invalid Input, please try again.\n")
                continue
            novalid_input3 = False
        return(operation_input, number1_input, number2_input)
    except NameError:
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
        operation_input = re.sub(r'\d+', '', operation_input.strip().lower())
        if (operation_input not in operators) or (operation_input == "") or operation_input == None:
            print("Invalid Input, please try again.\n"
                  "Reference the attached table for valid inputs.\n")
            continue
        if operators[operation_input] == "exit":
            return ("exit", None, None)
        novalid_input1 = False
    while (novalid_input2):
        try:
            number1_input = float(
                re.sub(r'[^0-9,.]', '', input("Please enter the first number in the chosen operation.\n: ")))
        except:
            print("Invalid Input, please try again.\n")
            continue
        if number1_input == "" or number1_input == None:
            print("Invalid Input, please try again.\n")
            continue
        novalid_input2 = False
    while (novalid_input3):
        try:
            number2_input = float(
                re.sub(r'[^0-9,.]', '', input("Please enter the second number in the chosen operation.\n: ")))
        except:
            print("Invalid Input, please try again.\n")
            continue
        if number2_input == "" or number2_input == None:
            print("Invalid Input, please try again.\n")
            continue
        novalid_input3 = False
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
    run = True
    while run:
        operator_input, number1_input, number2_input = get_user_input()
        op = ""
        if operators[operator_input] == "exit":
            run = False
            print("Exiting...")
            break
        op_symbol = ops_to_symbols[operators[operator_input]]
        value = 0
        num1 = 0
        num2 = 0
        if op_symbol == ">>" or op_symbol == "<<":

            try:
                num1 = int(number1_input)
                num2 = int(number2_input)
            except:
                print("An unexpected error occurred. Please try again.\n"
                      "Note: The selected operation does not support floats.")
                continue

            if (not float.is_integer(number1_input)) and (not float.is_integer(number2_input)):
                print("One or more input numbers are a non-integer.\n"
                      "Non-integers are not supported for this operation.\n"
                      "Casting to integer.")

        else:
            num1 = number1_input
            num2 = number2_input
        value = operators[operator_input](num1, num2)
        print(f"\n\nOutput:\n {number1_input} {op_symbol} {number2_input} = {value:.5f}\n")


