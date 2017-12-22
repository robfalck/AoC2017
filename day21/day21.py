from __future__ import print_function, division, absolute_import

import re
import time
import numpy as np


np.set_printoptions(linewidth=1024, edgeitems=9)

def decode_pattern(pattern, sep='/'):
    n = len(pattern.split(sep))
    mat = np.zeros((n, n), dtype=int)
    for i, line in enumerate(pattern.split(sep)):
        for j, char in enumerate(line.strip()):
            if char == '#':
                mat[i, j] = 1
    return mat

def encode_pattern(mat):
    """
    Encode the matrix into a hashable value.
    """
    return tuple(mat.flatten().tolist())

def initialize_rulebook(inp):
    rulebook = {}

    for line in inp:
        in_, out_ = line.split('=>')

        out_mat = decode_pattern(out_)

        # permute all possible configurations of in_
        in_mat = decode_pattern(in_)

        rot0 = in_mat
        rot90 = np.rot90(in_mat)
        rot180 = np.rot90(rot90)
        rot270 = np.rot90(rot180)

        rot0_lr = np.fliplr(rot0)
        rot90_lr = np.fliplr(rot90)
        rot180_lr = np.fliplr(rot180)
        rot270_lr = np.fliplr(rot270)

        rot0_ud = np.flipud(rot0)
        rot90_ud = np.flipud(rot90)
        rot180_ud = np.flipud(rot180)
        rot270_ud = np.flipud(rot270)

        rulebook[encode_pattern(rot0)] = out_mat
        rulebook[encode_pattern(rot90)] = out_mat
        rulebook[encode_pattern(rot180)] = out_mat
        rulebook[encode_pattern(rot270)] = out_mat

        rulebook[encode_pattern(rot0_lr)] = out_mat
        rulebook[encode_pattern(rot90_lr)] = out_mat
        rulebook[encode_pattern(rot180_lr)] = out_mat
        rulebook[encode_pattern(rot270_lr)] = out_mat

        rulebook[encode_pattern(rot0_ud)] = out_mat
        rulebook[encode_pattern(rot90_ud)] = out_mat
        rulebook[encode_pattern(rot180_ud)] = out_mat
        rulebook[encode_pattern(rot270_ud)] = out_mat

    return rulebook

def solve(inp, num_iter=2):
    start = '.#.\n..#\n###'

    rulebook = initialize_rulebook(inp)

    # for key in rulebook:
    #     print(key)

    image = decode_pattern(start, '\n')

    for iter in range(num_iter):
        print('iter:', iter)
        num_rows = image.shape[0]

        # Extract blocks
        in_blocks = []

        print('  num_rows:', num_rows)

        for divisor in (2, 3):
            if num_rows % divisor == 0:
                vblocks = np.vsplit(image, num_rows // divisor)
                print('broken into #rows:', num_rows // divisor)
                for vblock in vblocks:
                    hblocks = np.hsplit(vblock, num_rows // divisor)
                    block_row = []
                    for hblock in hblocks:
                        block_row.append(hblock)
                    in_blocks.append(block_row)
                break


        # Find the replacement blocks
        out_blocks = []
        for in_block_row in in_blocks:
            out_block_row = []
            for block in in_block_row:
                pattern = encode_pattern(block)
                out_block_row.append(rulebook[pattern])
            out_blocks.append(out_block_row)

        # print(out_blocks)
        # Assemble replacement blocks into new image
        image = np.block(out_blocks)

    print('num nonzero:', np.count_nonzero(image))







if __name__ == '__main__':


    with open('input.txt', 'r') as f:
        puzzle_input = [line.strip() for line in f.readlines() if line]

    t0 = time.time()
    solve(puzzle_input, 5)
    print('Time to solve part 1:', time.time()-t0, 'sec')

    t0 = time.time()
    solve(puzzle_input, 18)  # 2301762
    print('Time to solve part 2:', time.time()-t0, 'sec')
