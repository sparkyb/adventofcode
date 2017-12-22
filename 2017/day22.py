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

    return input.split('\n')
# end get_input

def part1(grid):
    x = len(grid[0])/2
    y = len(grid)/2
    dx = 0
    dy = -1
    state = dict(((x2,y2),c) for y2,row in enumerate(grid) for x2,c in enumerate(row))
    count = 0
    for i in xrange(10000):
        cur = state.get((x,y),'.')
        if cur == '#':
            dx, dy = -dy, dx
            state[(x,y)] = '.'
        else:
            dx, dy = dy, -dx
            state[(x,y)] = '#'
            count += 1
        x += dx
        y += dy
    return count
# end part1

def part2(grid):
    x = len(grid[0])/2
    y = len(grid)/2
    dx = 0
    dy = -1
    state = dict(((x2,y2),c) for y2,row in enumerate(grid) for x2,c in enumerate(row))
    count = 0
    for i in xrange(10000000):
        cur = state.get((x,y),'.')
        if cur == '#':
            dx, dy = -dy, dx
            state[(x,y)] = 'F'
        elif cur == 'F':
            dx, dy = -dx, -dy
            state[(x,y)] = '.'
        elif cur == 'W':
            state[(x,y)] = '#'
            count += 1
        else:
            dx, dy = dy, -dx
            state[(x,y)] = 'W'
        x += dx
        y += dy
    return count
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

