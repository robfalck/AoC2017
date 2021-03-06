from __future__ import print_function, division, absolute_import

import numpy as np

drow = {'n': -1,
        'e': 0,
        's': 1,
        'w': 0}

dcol = {'n': 0,
        'e': 1,
        's': 0,
        'w': -1}

class Mover(object):

    def __init__(self, mat):
        rows, cols = mat.shape
        for col in range(cols):
            if mat[0, col] == '|':
                self.row, self.col = 0, col

        self.heading = 's'
        self.sequence = ''
        self.mat = mat
        self.finished = False
        self.steps = 0

    def take_step(self):
        self.row += drow[self.heading]
        self.col += dcol[self.heading]
        self.steps += 1
        try:
            if self.mat[self.row, self.col] == ' ':
                self.finished = True
        except IndexError:
            self.finished = True


    def check_for_letter(self):
        char = self.mat[self.row, self.col]
        if char.isalpha():
            print('found alpha:', char)
            self.sequence += char

    def is_opposite_direction(self, direction):
        if self.heading == 'n' and direction == 's':
            return True
        if self.heading == 's' and direction == 'n':
            return True
        if self.heading == 'e' and direction == 'w':
            return True
        if self.heading == 'w' and direction == 'e':
            return True
        return False

    def find_new_heading(self):
        directions = 'n', 's', 'e', 'w'
        for d in directions:
            if self.is_opposite_direction(d):
                continue
            try:
                if self.mat[self.row + drow[d], self.col + dcol[d]] != ' ':
                    return d
            except:
                pass
        self.finished = True

    def check_for_fork(self):
        return self.mat[self.row, self.col] == '+'

    def walk(self):
        while not self.finished:
            print(self.row, self.col, self.heading)
            self.take_step()
            self.check_for_letter()
            if self.check_for_fork():
                self.heading = self.find_new_heading()


def load_matrix(inp):

    num_rows = len(inp)
    num_cols = max([len(inp[i]) for i in range(len(inp))])

    ar = np.empty((num_rows, num_cols), dtype=str)

    ar[:, :] = ' '

    row = 0
    for line in inp:
        for col, char in enumerate(line):
            ar[row, col] = char
        row += 1

    return ar


def solve(inp):
    mat = load_matrix(inp)

    print(mat)

    m = Mover(mat)

    m.walk()

    print('sequence:', m.sequence)
    print('num steps:', m.steps)


if __name__ == '__main__':


    with open('test_input.txt', 'r') as f:
        puzzle_input = [line.rstrip() for line in f.readlines()]

    solve(puzzle_input)



    with open('input.txt', 'r') as f:
        puzzle_input = [line.rstrip() for line in f.readlines()]

    solve(puzzle_input)