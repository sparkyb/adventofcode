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
        input = fp.read()

    return input.split('\n')
# end get_input

def walk_grid(grid):
    y = 0
    x = grid[0].index('|')
    dx = 0
    dy = 1
    letters = ''
    steps = 1
    while True:
        while grid[y][x] != '+':
            if grid[y][x].isalpha():
                letters += grid[y][x]
            if grid[y+dy][x+dx] == ' ':
                return letters, steps
            x += dx
            y += dy
            steps += 1
        assert grid[y+dy][x+dx] == ' '
        if dy:
            dy = 0
            if grid[y][x+1] == ' ':
                assert grid[y][x-1] != ' '
                dx = -1
            else:
                assert grid[y][x-1] == ' '
                dx = 1
        else:
            dx = 0
            if grid[y+1][x] == ' ':
                assert grid[y-1][x] != ' '
                dy = -1
            else:
                assert grid[y-1][x] == ' '
                dy = 1
        x += dx
        y += dy
        steps += 1
# end walk_grid

def part1(grid):
    return walk_grid(grid)[0]
# end part1

def part2(grid):
    return walk_grid(grid)[1]
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

