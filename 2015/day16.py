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

    return dict((int(groups[0]),dict((k, int(v)) for k,v in zip(groups[1::2],groups[2::2]))) for groups in (re.search(r'^Sue (\d+): (\w+): (\d+), (\w+): (\d+), (\w+): (\d+)$', line).groups() for line in input.split('\n')))
# end get_input

def part1(sues):
    unknown = {
        'children': 3,
        'cats': 7,
        'samoyeds': 2,
        'pomeranians': 3,
        'akitas': 0,
        'vizslas': 0,
        'goldfish': 5,
        'trees': 3,
        'cars': 2,
        'perfumes': 1,
    }
    for i,sue in sues.items():
        for k,v in sue.items():
            if v != unknown[k]:
                break
        else:
            return i
# end part1

def part2(sues):
    unknown = {
        'children': 3,
        'cats': 7,
        'samoyeds': 2,
        'pomeranians': 3,
        'akitas': 0,
        'vizslas': 0,
        'goldfish': 5,
        'trees': 3,
        'cars': 2,
        'perfumes': 1,
    }
    for i,sue in sues.items():
        for k,v in sue.items():
            if k in ('cats','trees'):
                if v <= unknown[k]:
                    break
            elif k in ('pomeranians','goldfish'):
                if v >= unknown[k]:
                    break
            elif v != unknown[k]:
                break
        else:
            return i
# end part2

if __name__ == '__main__':
    sues = get_input()
    print part1(sues)
    print part2(sues)

