import os.path
import re
import math
from collections import defaultdict
from itertools import permutations,combinations


def get_input(filename=None):
    if not filename:
        filename = os.path.splitext(os.path.basename(__file__))[0]+'.txt'
    with open(filename) as fp:
        input = fp.read().strip()

    return map(int, input.split('\n'))
# end get_input

def part1(containers):
    count = 0
    for i in xrange(1,len(containers)):
        for items in combinations(containers,i):
            if sum(items) == 150:
                count += 1
    return count
# end part1

def part2(containers):
    count = 0
    for i in xrange(1,len(containers)):
        for items in combinations(containers,i):
            if sum(items) == 150:
                count += 1
        if count:
            break
    return count
# end part2

if __name__ == '__main__':
    containers = get_input()
    print part1(containers)
    print part2(containers)

