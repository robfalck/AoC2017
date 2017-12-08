from __future__ import print_function, division, absolute_import

from six import iterkeys
import numpy as np

# Functions to compute our conditions (borrowed from numpy)
condition_funcs = {'>': np.greater,
                   '>=': np.greater_equal,
                   '<': np.less,
                   '<=': np.less_equal,
                   '==': np.equal,
                   '!=': np.not_equal}

# Functions to perform the increment/decrement (borrowed from numpy)
instruction_funcs = {'inc' : np.add,
                     'dec' : np.subtract}

def solve(input):
    """
    Solve the Day 08 puzzle.

    Loop through the list of instructions, using a simple split to extract
    each portion of the instruction.

    Registers are stored in a dictionary.  If we encounter a previously unknown
    register name, put it in the dictionary with a value of 0.

    The maximum value is extracted from the dictionary the max function
    to return the max *key*, where the comparator for the key is obtained
    with the function `registers[key]`.  (The fact that the argument to
    max that defines the comparator is `key` makes this a bit confusing).

    max_key = max(iterkeys(registers), key=lambda k: registers[k])

    For part 2 it's just a matter of doing this after every instruction rather
    than at the end of the loop, and saving the all-time greatest value.


    Parameters
    ----------
    input

    Returns
    -------
    max_key : str
        The key with the maximum value at the end of the instructions.
    max_val : int
        The maximum value of any register at the end of the instructions.
    all_time_max_key : str
        The register which had the largest value at any interation of the instructions.
    all_time_max_val : int
        The maxium value of any register at any iteration of the instructions.
    """
    registers = {}

    all_time_max_val = -1000000000000
    all_time_max_key = ''

    for line in input:
        reg, instruction, amount, _, reg_to_test, cond, cond_amount = line.split()
        amount = int(amount)
        cond_amount = int(cond_amount)

        if reg not in registers:
            registers[reg] = 0
        if reg_to_test not in registers:
            registers[reg_to_test] = 0

        if condition_funcs[cond](registers[reg_to_test], cond_amount):
            registers[reg] = instruction_funcs[instruction](registers[reg], amount)

        max_key = max(iterkeys(registers), key=lambda k: registers[k])
        max_val = registers[max_key]

        if max_val > all_time_max_val:
            all_time_max_val = max_val
            all_time_max_key = max_key

    return max_key, registers[max_key], all_time_max_key, all_time_max_val


if __name__ == '__main__':
    with open('test_input.txt', 'r') as f:
        test_input = f.readlines()
    print(solve(test_input))

    with open('input.txt', 'r') as f:
        test_input = f.readlines()
    print(solve(test_input))
