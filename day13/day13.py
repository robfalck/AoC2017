from __future__ import print_function, division, absolute_import

import time
import numpy as np

# Columns of our scanner matrix data structure
DEPTH, RANGE, POS, VEL, DETECTION = range(5)

def advance_scanners(scanners):

    scanners[:, 2] += scanners[:, 3]

    idxs_to_reverse = np.where(np.logical_and(scanners[:, VEL] == 1,
                                              scanners[:, POS] == scanners[:, RANGE] - 1))[0]
    scanners[idxs_to_reverse, 3] *= -1

    idxs_to_reverse = np.where(np.logical_and(scanners[:, VEL] == -1,
                                              scanners[:, POS] == 0))[0]
    scanners[idxs_to_reverse, 3] *= -1


def check_detection(packet_depth, scanners):

    detecting_scanner = np.where(scanners[:, 0] == packet_depth)[0]
    if scanners[detecting_scanner, POS] == 0:
        scanners[detecting_scanner, DETECTION] += 1


def was_detected(scanners):
    return np.any(scanners[:, DETECTION] > 0)

def severity(scanners):
    score = np.dot(scanners[:, 4], scanners[:, 0] * scanners[:, 1])
    return score


def solve(puzzle_input):

    firewall = [line.split(':') for line in puzzle_input if line]
    firewall = [(int(row[0].strip()), int(row[1].strip())) for row in firewall]

    scanners = np.zeros((len(firewall), 5), dtype=int)
    scanners[:, :2] = firewall
    scanners[:, VEL] = 1

    firewall_depth = np.max(scanners[:, DEPTH]) + 1

    # Part 1
    packet_depth = 0
    clock = 0

    while True:
        if packet_depth in scanners[:, DEPTH]:
            check_detection(packet_depth, scanners)
        advance_scanners(scanners)
        packet_depth += 1
        clock += 1
        if packet_depth >= firewall_depth:
            break

    print('Severity of Trip:', severity(scanners))  # 2264

    # Part 2

    for delay in range(1000000000):
        if delay % 10000 == 0:
            print(delay)

        # Reinitialize the firewall
        scanners[:, POS] = 0
        scanners[:, VEL] = 1
        scanners[:, DETECTION] = 0

        if delay > 0:
            scanners[:, :] = scanners_after_delay[:, :]
            advance_scanners(scanners)

        # Cache the scanner state after the delay so
        # we don't have to reinitialize the whole thing
        # the next time through.
        scanners_after_delay = scanners.copy()

        packet_depth = 0
        clock = 0

        while True:
            if packet_depth in scanners[:, DEPTH]:
                check_detection(packet_depth, scanners)
            if was_detected(scanners):
                break
            advance_scanners(scanners)
            packet_depth += 1
            clock += 1
            if packet_depth >= firewall_depth:
                break

        if not was_detected(scanners):
            print('Success with delay =', delay)
            break
    else:
        print('no successful delay found')




if __name__ == '__main__':

    with open('test_input.txt', 'r') as f:
        test_input = f.readlines()

    solve(test_input)

    print()

    with open('input.txt', 'r') as f:
        puzzle_input = f.readlines()

    t0 = time.time()
    solve(puzzle_input)
    print('Time for solution:', time.time()-t0)

