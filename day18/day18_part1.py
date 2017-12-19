from __future__ import print_function, division, absolute_import



def _decode_y(y, registers):
    try:
        return int(y)
    except ValueError:
        return registers.get(y, 0)


class Program(object):

    def __init__(self, inp):
        self.instructions = []
        for line in inp:
            inst, *args = line.split()
            self.instructions.append((inst, args))

        self.registers = {}
        self.last_freq = 0
        self.idx = 0
        self.jump_depth = 0

        self.instruction_map = {'snd': self.snd,
                                'set': self.set,
                                'add': self.add,
                                'mul': self.mul,
                                'mod': self.mod,
                                'rcv': self.rcv,
                                'jgz': self.jgz}

    def snd(self, y):
        print('    snd', y)
        self.last_freq = _decode_y(y, self.registers)
        self.idx += 1

    def set(self, x, y):
        print('    set', x, y)
        self.registers[x] = _decode_y(y, self.registers)
        self.idx += 1

    def add(self, x, y):
        print('    add', x, y)
        self.registers[x] = self.registers.get(x, 0) + _decode_y(y, self.registers)
        self.idx += 1

    def mul(self, x, y):
        print('    mul', x, y)
        self.registers[x] = self.registers.get(x, 0) * _decode_y(y, self.registers)
        self.idx += 1

    def mod(self, x, y):
        print('    mod', x, y)
        self.registers[x] = self.registers.get(x, 0) % _decode_y(y, self.registers)
        self.idx += 1

    def rcv(self, x):
        print('    rcv', x, self.registers.get(x, 0))
        if self.registers.get(x, 0) != 0:
            print('    last frequency played:', self.last_freq)
            exit(0)
        else:
            print('    SKIP')
        self.idx += 1

    def jgz(self, x, y):
        print('    jgz', x, y)

        if self.registers.get(x, 0) > 0:
            self.idx = self.idx + _decode_y(y, self.registers)
            # if self.idx < 0 or self.idx > len(self.instructions):
            #     print('    jumped off of instruction table')
            #     exit(0)
            # inst, args = self.instructions[self.idx]
            # self.instruction_map[inst](*args)
        else:
            print('    SKIP')
            self.idx += 1

    def run(self):

        self.idx = 0

        while 0 <= self.idx < len(self.instructions):
            print(self.idx)
            inst, args = self.instructions[self.idx]
            self.instruction_map[inst](*args)
            print('    ', self.registers)  # 8600



def solve(inp):

    iset = Program(inp)

    iset.run()




if __name__ == '__main__':

    # with open('test_input.txt', 'r') as f:
    #     test_input = [line for line in f.readlines() if line]
    #
    # solve(test_input)

    print()

    with open('input.txt', 'r') as f:
        puzzle_input = [line for line in f.readlines() if line]

    solve(puzzle_input)