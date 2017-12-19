from __future__ import print_function, division, absolute_import

from multiprocessing import Process, Queue, Manager

try:
    from queue import Empty
except:
    from Queue import Empty

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
        self.log = None

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
        self.send_count += 1
        self.log['send_count_{0}'.format(self.id)] = self.send_count
        self.output_queue.put(self.decode_y(y))
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
        self.registers[x] = self.input_queue.get(timeout=1)
        self.idx += 1

    def jgz(self, x, y):
        if x.isalpha():
            reg_name = x
        else:
            reg_name = chr(int(x)+97)

        if self.registers.get(reg_name, 0) > 0:
            self.idx = self.idx + self.decode_y(y)
        else:
            self.idx += 1

    def run(self, log):
        self.log = log
        while not self.is_finished():
            inst, args = self.instructions[self.idx]
            try:
                self.instruction_map[inst](*args)
            except Empty:
                break

    def is_finished(self):
        return (self.idx < 0) or (self.idx >= len(self.instructions))



def solve(inp):

    program_0 = Program(inp, 0)
    program_1 = Program(inp, 1)

    program_0.input_queue = program_1.output_queue = Queue()
    program_1.input_queue = program_0.output_queue = Queue()

    mgr = Manager()
    d = mgr.dict()

    process_0 = Process(target=program_0.run, args=(d,))
    process_1 = Process(target=program_1.run, args=(d,))

    process_0.start()
    process_1.start()

    process_0.join()
    process_1.join()

    print(d)


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