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
    """
    Solve the Day 11 puzzle given an input string.

    Parameters
    ----------
    puzzle_input : str
        A comma-separated list of directions to take in a hex-grid
        where the hexes are oriented with the flat sides aligned north-south.

    Returns
    -------
    final_distance : int
        The distance from the origin for the final step.
    max_distance : int
        The maximum distance from the origin for any step.

    """
    origin = Hex(0, 0)
    next_hex = origin
    max_distance = 0

    for step in puzzle_input.split(','):
        q_offset, r_offset = qr_offset[step]
        next_hex = Hex(next_hex.q + q_offset, next_hex.r + r_offset)
        manh_dist = next_hex.distance_to_origin()
        if manh_dist > max_distance:
            max_distance = manh_dist

    return next_hex.distance_to_origin(), max_distance


if __name__ == '__main__':

    assert(solve('ne,ne,ne') == (3, 3))
    assert(solve('ne,ne,sw,sw') == (0, 2))
    assert(solve('ne,ne,s,s') == (2, 2))
    assert(solve('se,sw,se,sw,sw') == (3, 3))

    with open('input.txt', 'r') as f:
        puzzle_input = f.readlines()[0].strip()

    final_distance, max_distance = solve(puzzle_input)
    print('Final Distance:', final_distance)
    print('Max Distance:', max_distance)
