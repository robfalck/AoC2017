from __future__ import print_function, division, absolute_import


class Program(object):

    def __init__(self, inp, id):
        self.instructions = []
        for line in inp:
            inst, *args = line.split()
            self.instructions.append((inst, args))

        self.id = id
        self.registers = {'p': id}
        self.idx = 0
        self.input_queue = None
        self.output_queue = None
        self.send_count = 0
        self.waiting = False
        self.stop = False

        self.instruction_map = {'snd': self.snd,
                                'set': self.set,
                                'add': self.add,
                                'mul': self.mul,
                                'mod': self.mod,
                                'rcv': self.rcv,
                                'jgz': self.jgz}

    def decode_y(self, y):
        try:
            return int(y)
        except ValueError:
            return self.registers.get(y, 0)

    def snd(self, y):
        self.output_queue.append(self.decode_y(y))
        if self.id == 1:
            print(1, 'snd', self.decode_y(y), self.output_queue)
            pass
        self.send_count += 1
        self.idx += 1

    def set(self, x, y):
        self.registers[x] = self.decode_y(y)
        self.idx += 1

    def add(self, x, y):
        self.registers[x] = self.registers.get(x, 0) + self.decode_y(y)
        self.idx += 1

    def mul(self, x, y):
        self.registers[x] = self.registers.get(x, 0) * self.decode_y(y)
        self.idx += 1

    def mod(self, x, y):
        self.registers[x] = self.registers.get(x, 0) % self.decode_y(y)
        self.idx += 1

    def rcv(self, x):
        if self.input_queue:
            self.registers[x] = self.input_queue.pop(0)
            self.idx += 1
            self.waiting = False
        else:
            self.waiting = True

    def jgz(self, x, y):
        if x.isalpha():
            reg_name = x
        else:
            reg_name = chr(int(x)+97)

        if self.registers.get(reg_name, 0) > 0:
            self.idx = self.idx + self.decode_y(y)
        else:
            self.idx += 1

    def execute_next(self):
        inst, args = self.instructions[self.idx]
        self.instruction_map[inst](*args)

    def is_finished(self):
        return (self.idx < 0) or (self.idx >= len(self.instructions))

    def is_waiting(self):
        return self.waiting


def solve(inp):

    program_0 = Program(inp, 0)
    program_1 = Program(inp, 1)

    program_0.input_queue = program_1.output_queue = []
    program_1.input_queue = program_0.output_queue = []

    i = 0

    while not program_1.is_finished() and not program_0.is_finished():
        program_1.execute_next()
        program_0.execute_next()
        i += 1
        print(program_1.idx, program_1.registers)
        if program_0.is_waiting() and program_1.is_waiting():
            # Deadlock!
            break

    print(program_0.send_count, program_1.send_count)


if __name__ == '__main__':

    # with open('test_input2.txt', 'r') as f:
    #     puzzle_input = [line for line in f.readlines() if line]
    #
    # solve(puzzle_input)
    #
    # print()

    with open('input.txt', 'r') as f:
        puzzle_input = [line for line in f.readlines() if line]

    solve(puzzle_input)