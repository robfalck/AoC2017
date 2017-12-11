from __future__ import print_function, division, absolute_import


class Hex(object):
    """
    A "Hex" location in a hexagonal grid, specified by axial coordinates as detailed
    here:  https://www.redblobgames.com/grids/hexagons/implementation.html

    Parameters
    ----------
    q : int
        The axial column q of the hex in the grid.
    r : int
        The axial row r of the hex in the grid.
    """
    def __init__(self, q, r):
        self.q = q
        self.r = r

    @property
    def s(self):
        """
        Parameter s in the coordinates, such that
        s = -q - r
        """
        return - self.q - self.r

    def __add__(self, other):
        return Hex(self.q + other.q, self.r + other.r, self.s + other.s)

    def __sub__(self, other):
        return Hex(self.q - other.q, self.r - other.r, self.s - other.s)

    def distance_to_origin(self):
        """
        Returns the distance to the origin of the hex.
        """
        return (abs(self.q) + abs(self.r) + abs(self.s)) // 2

    def distance_to(self, other):
        """
        Returns the distance to the hex given by other.
        """
        return (self - other).distance_to_origin()

    def manhattan_distance_to(self, other):
        """
        Returns the Manhattan distance to the hex given by other.
        """
        return (abs(self.q - other.q) + abs(self.r - other.r) + abs(self.s - other.s)) // 2

    def __repr__(self):
        return 'Hex({0}, {1}, {2})'.format(self.q, self.r, self.s)


qr_offset = {'n': (0, -1),
             'ne': (1, -1),
             'se': (1, 0),
             's': (0, 1),
             'sw': (-1, 1),
             'nw': (-1, 0)}


def solve(puzzle_input):

    origin = Hex(0, 0)
    next_hex = origin

    max_distance = 0

    for step in puzzle_input.split(','):
        q_offset, r_offset = qr_offset[step]
        next_hex = Hex(next_hex.q + q_offset, next_hex.r + r_offset)
        manh_dist = origin.manhattan_distance_to(next_hex)
        if manh_dist > max_distance:
            max_distance = manh_dist

    return origin.manhattan_distance_to(next_hex), max_distance






if __name__ == '__main__':

    # assert(solve('ne,ne,ne') == 3)
    # assert(solve('ne,ne,sw,sw') == 0)
    print(solve('ne,ne,s,s'))
    print(solve('se,sw,se,sw,sw'))


    with open('input.txt', 'r') as f:
        puzzle_input = f.readlines()[0].strip()

    print(solve(puzzle_input))