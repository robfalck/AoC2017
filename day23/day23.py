from __future__ import print_function, division, absolute_import

import time
import numpy as np


class Program(object):

    def __init__(self, inp, id=0):
        self.instructions = []
        for line in inp:
            inst, *args = line.split()
            self.instructions.append((inst, args))

        self.id = id
        self.registers = [ 0 for _ in 'abcdefgh']
        self.idx = 0
        self.mul_count = 0
        self.tick = 0

        self.instruction_map = {'set': self.set,
                                'sub': self.sub,
                                'mul': self.mul,
                                'jnz': self.jnz}

    def decode_y(self, y):
        try:
            return int(y)
        except ValueError:
            return self.registers[ord(y)-97]

    def register_to_int(self, register):
        if register.isalpha():
            return ord(register) - 97
        elif register.isnumeric():
            return int(register)
        else:
            raise ValueError('Unexpected register')

    def set(self, x, y):
        self.registers[self.register_to_int(x)] = self.decode_y(y)
        self.idx += 1

    def sub(self, x, y):
        self.registers[self.register_to_int(x)] -= self.decode_y(y)
        self.idx += 1

    def mul(self, x, y):
        self.registers[self.register_to_int(x)] *= self.decode_y(y)
        self.mul_count += 1
        self.idx += 1

    def jnz(self, x, y):
        if self.registers[self.register_to_int(x)] != 0:
            # print('at line', self.idx, 'jump', self.decode_y(y))
            self.idx = self.idx + self.decode_y(y)
        else:
            self.idx += 1

    def execute_next(self):
        inst, args = self.instructions[self.idx]
        self.instruction_map[inst](*args)
        self.tick += 1

    def is_finished(self):
        return (self.idx < 0) or (self.idx >= len(self.instructions))

    def run(self, part=1):
        self.registers = [ 0 for _ in 'abcdefgh']
        self.idx = 0
        self.mul_count = 0
        self.tick = 0

        if part == 2:
            self.registers[self.register_to_int('a')] = 1

        while not self.is_finished():
            self.execute_next()




def solve(inp, part=1):

    p = Program(inp)
    p.run(part=part)
    print('Multiplication count:', p.mul_count)
    print('Registers:')
    for i, reg in enumerate('abcdefgh'):
        print('    ', reg, p.registers[i])



if __name__ == '__main__':


    with open('input.txt', 'r') as f:
        puzzle_input = [line.strip() for line in f.readlines() if line and not line.startswith('#')]

    t0 = time.time()
    solve(puzzle_input, part=1)
    print('Time to solve part 1:', time.time()-t0, 'sec')
    #
    # t0 = time.time()
    # solve(puzzle_input, part=2)
    # print('Time to solve part 2:', time.time()-t0, 'sec')
