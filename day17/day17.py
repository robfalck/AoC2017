from __future__ import print_function, division, absolute_import


class SpinLock(object):

    def __init__(self):
        self.buffer = [0]
        self.current_idx = 0
        self.max_val = 0

    def spin(self, n):
        # print('start:', self.buffer, self.buffer[self.current_idx])
        for i in range(n):
            self.current_idx += 1
            if self.current_idx >= len(self.buffer):
                self.current_idx = 0
            # print('    ', self.current_idx)
        if self.current_idx < len(self.buffer) - 1:
            self.buffer.insert(self.current_idx + 1, len(self.buffer))
            self.current_idx += 1
            if self.current_idx == 1:
                print(self.buffer[1])
        else:
            self.buffer.insert(len(self.buffer), len(self.buffer))
            self.current_idx = len(self.buffer)-1
        # print('end:', self.buffer, self.buffer[self.current_idx])

class SpinLock2(object):

    def __init__(self):
        self.current_idx = 0
        self.buf_size = 1

    def spin(self, n):
        # print('start:', self.buffer, self.buffer[self.current_idx])
        for i in range(n):
            self.current_idx += 1
            if self.current_idx >= self.buf_size:
                self.current_idx = 0
            # print('    ', self.current_idx)
        if self.current_idx < self.buf_size - 1:
            #self.buffer.insert(self.current_idx + 1, self.buf_size)
            self.buf_size += 1
            self.current_idx += 1
            if self.current_idx == 1:
                print(self.buf_size-1)
        else:
            # self.buffer.insert(len(self.buffer), len(self.buffer))
            self.buf_size += 1
            self.current_idx = self.buf_size-1
        # print('end:', self.buffer, self.buffer[self.current_idx])


def solve(inp):

    sp = SpinLock()

    for i in range(2017):
        sp.spin(3)

    idx_2017 = sp.buffer.index(2017)

    if idx_2017 == len(sp.buffer)-1:
        idx_result = 0
    else:
        idx_result = idx_2017 + 1

    print('Test Solution:', sp.buffer[idx_result])

    ### Part 1

    sp = SpinLock()

    for i in range(2017):
        sp.spin(304)

    idx_last = sp.buffer.index(2017)

    print(idx_last)

    if idx_last == len(sp.buffer)-1:
        idx_result = 0
    else:
        idx_result = idx_last + 1

    print('Solution:', sp.buffer[idx_result])

    ### Part 2

    sp2 = SpinLock2()

    for i in range(5000000):
        sp2.spin(304)
        #print(i+1, sp.buffer[1])

    print('Solution:', sp2.buffer[1])



if __name__ == '__main__':

    solve(None)

    # with open('input.txt', 'r') as f:
    #     puzzle_input = f.readlines()
    #
    # solve(puzzle_input)