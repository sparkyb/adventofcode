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

    return input.split(',')
# end get_input

def dist(x, y):
    x = abs(x)
    y = abs(y)
    y = max(y-x/2,0)
    return x + y

def part1(input):
    x, y = 0, 0
    for dir in input:
        if dir == 'n':
            y -= 1
        elif dir == 's':
            y += 1
        elif dir == 'nw':
            if x % 2:
                y -= 1
            x -= 1
        elif dir == 'sw':
            if x % 2 == 0:
                y += 1
            x -= 1
        elif dir == 'ne':
            if x % 2:
                y -= 1
            x += 1
        elif dir == 'se':
            if x % 2 == 0:
                y += 1
            x += 1
    return dist(x, y)
# end part1

def part2(input):
    x, y = 0, 0
    maxdist = 0
    for dir in input:
        if dir == 'n':
            y -= 1
        elif dir == 's':
            y += 1
        elif dir == 'nw':
            if x % 2:
                y -= 1
            x -= 1
        elif dir == 'sw':
            if x % 2 == 0:
                y += 1
            x -= 1
        elif dir == 'ne':
            if x % 2:
                y -= 1
            x += 1
        elif dir == 'se':
            if x % 2 == 0:
                y += 1
            x += 1
        maxdist = max(dist(x,y),maxdist)
    return maxdist
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

