import os.path
import re
import math
from collections import defaultdict
from itertools import permutations


def get_input(filename=None):
    if not filename:
        filename = os.path.splitext(os.path.basename(__file__))[0]+'.txt'
    with open(filename) as fp:
        input = fp.read().strip()

    return input.split('\n')
# end get_input

def part1(input):
    return None
# end part1

def part2(input):
    return None
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

