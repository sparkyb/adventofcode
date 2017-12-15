import os.path
import re
import math
from collections import defaultdict
import itertools
import md5


def get_input(filename=None):
    if not filename:
        filename = os.path.splitext(os.path.basename(__file__))[0]+'.txt'
    with open(filename) as fp:
        input = fp.read().strip()

    return dict((int(n), map(int, l.split(', '))) for n, l in (re.search(r'^(\d+) <-> (\d+(?:, \d+)*)$', line).groups() for line in input.split('\n')))
# end get_input

def findgroup(input, start):
    group = set()
    frontier = [start]
    while frontier:
        i = frontier.pop(0)
        group.add(i)
        for j in input[i]:
            if j not in group and j not in frontier:
                frontier.append(j)
    return group

def part1(input):
    return len(findgroup(input, 0))
# end part1

def part2(input):
    all = set()
    count = 0
    for i in input:
        if i in all:
            continue
        count += 1
        all.update(findgroup(input, i))
    return count
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

