from __future__ import print_function, division, absolute_import

import numpy as np


def spin(x, dancers):
    """
    Remove x characters from the end of the string
    and place them, order unchanged, on the front.

    Parameters
    ----------
    x : int
        Number of characters to be moved from end of dancers
        to the front of dancers.
    dancers : str
        A mutable sequence of characters
    """
    end = dancers[-x:]
    return end + dancers[:len(dancers)-x]


def exchange(a, b, dancers):
    """
    Swap places of dancers a and b.

    Parameters
    ----------
    a : int
        Index of the first character to be swapped
    b : int
        Index of the second character to be swapped
    dancers : list
        A mutable sequence of characters, modified in place.
    """
    dancer_list = [char for char in dancers]
    dancer_list[b], dancer_list[a] = dancer_list[a], dancer_list[b]
    return ''.join(dancer_list)


def partner(a, b, dancers):
    """
    Swap places of dancers named a and b.

    Parameters
    ----------
    a : str
        Name of the first character to be swapped
    b : str
        Name of the second character to be swapped
    dancers : list
        A mutable sequence of characters, modified in place.
    """
    a_idx = dancers.index(a)
    b_idx = dancers.index(b)
    dancer_list = [char for char in dancers]
    dancer_list[b_idx], dancer_list[a_idx] = dancer_list[a_idx], dancer_list[b_idx]
    return ''.join(dancer_list)

def solve(dancers, instructions, charset='abcdefghijklmnop', num_times=1, find_cycle=True):

    # print(''.join(dancers))
    #
    # print(len('instructions'))
    cycle_length = -1

    for j in range(num_times):
        for i, step in enumerate(instructions):
            move = step[0]
            if move == 's':
                x = int(step[1:])
                dancers = spin(x, dancers)
            elif move == 'x':
                a, b = step[1:].split('/')
                dancers = exchange(int(a), int(b), dancers)
            elif move == 'p':
                a, b = step[1:].split('/')
                dancers = partner(a, b, dancers)
        if find_cycle and dancers == 'abcdefghijklmnop':
            return None, None, j+1

    permutation = [charset.index(char) for char in dancers]

    return dancers, permutation, cycle_length


def test_solution(dancers, charset='abcdefghijklmnop'):
    flag = False
    #print('testing:', dancers)
    for char in charset:
        if char not in dancers:
            flag = True
            print('{0} not in dancers!'.format(char))
    if flag:
        print(''.join(dancers))
        raise ValueError('error')


def permute(n, seq, permutation):
    """
    This is the code to permute the solution without having to perform the 10000
    instruction sequence.
    """
    for i in range(n):
        seq = seq[permutation]
    return seq


def decode_permutation(chars, permutation):
    return ''.join([chars[i] for i in permutation])


if __name__ == '__main__':

    dancers = 'abcde'
    instructions = ['s1', 'x3/4', 'pe/b']

    sol, permutaion, _ = solve(dancers, instructions, charset='abcde')

    assert(sol == 'baedc')

    dancers = 'abcdefghijklmnop'

    with open('input.txt', 'r') as f:
        instructions = f.read().split(',')

    sol, permutation_1x, _ = solve(dancers, instructions)

    print('Solution', sol)  # iabmedjhclofgknp

    sol, _, _ = solve('abcdefghijklmnop', instructions, num_times=75, find_cycle=False)

    sol, _, cycle_length = solve(dancers, instructions,
                                              num_times=1000, find_cycle=True)

    print('Cycle Length:', cycle_length)

    sol, _, _ = solve('abcdefghijklmnop', instructions, num_times=1000000000 % cycle_length)

    print('Solution after 1E9 iterations:', sol)  # oildcmfeajhbpngk


