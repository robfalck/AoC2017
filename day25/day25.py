from __future__ import print_function, division, absolute_import

import time
from six import itervalues


def A(tape, pos):
    if tape.get(pos, 0) == 0:
        tape[pos] = 1
        pos += 1
        next_state = B
    else:
        tape[pos] = 0
        pos += 1
        next_state = C
    return pos, next_state


def B(tape, pos):
    if tape.get(pos, 0) == 0:
        tape[pos] = 0
        pos -= 1
        next_state = A
    else:
        tape[pos] = 0
        pos += 1
        next_state = D
    return pos, next_state


def C(tape, pos):
    if tape.get(pos, 0) == 0:
        tape[pos] = 1
        pos += 1
        next_state = D
    else:
        tape[pos] = 1
        pos += 1
        next_state = A
    return pos, next_state


def D(tape, pos):
    if tape.get(pos, 0) == 0:
        tape[pos] = 1
        pos -= 1
        next_state = E
    else:
        tape[pos] = 0
        pos -= 1
        next_state = D
    return pos, next_state


def E(tape, pos):
    if tape.get(pos, 0) == 0:
        tape[pos] = 1
        pos += 1
        next_state = F
    else:
        tape[pos] = 1
        pos -= 1
        next_state = B
    return pos, next_state


def F(tape, pos):
    if tape.get(pos, 0) == 0:
        tape[pos] = 1
        pos += 1
        next_state = A
    else:
        tape[pos] = 1
        pos += 1
        next_state = E
    return pos, next_state


def solve():
    tape = {0: 0}
    pos = 0
    next_state = A

    for i in range(12368930):
        pos, next_state = next_state(tape, pos)

    checksum = sum([val for val in itervalues(tape)])

    print('checksum = ', checksum)
    print(tape)


if __name__ == '__main__':

    t0 = time.time()
    solve()
    print('Time to solve test:', time.time()-t0, 'sec')
