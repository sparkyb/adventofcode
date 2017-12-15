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

    return [[c=='#' for c in line] for line in input.split('\n')]
# end get_input

def neighbors(lights, x, y):
    return sum(lights[y+dy][x+dx] for dy in (-1,0,1) if 0<=(y+dy)<len(lights) for dx in (-1,0,1) if 0<=(x+dx)<len(lights[y+dy]) and (dx,dy)!=(0,0))
# end neighbors

def step(lights):
    out = []
    for y,row in enumerate(lights):
        out_row = []
        for x,on in enumerate(row):
            count = neighbors(lights,x,y)
            if on:
                out_row.append(2<=count<=3)
            else:
                out_row.append(count==3)
        out.append(out_row)
    return out
# end step

def part1(lights):
    for i in xrange(100):
        lights = step(lights)
    return sum(sum(row) for row in lights)
# end part1

def part2(lights):
    lights = list(lights)
    lights[0][0] = True
    lights[0][-1] = True
    lights[-1][0] = True
    lights[-1][-1] = True
    for i in xrange(100):
        lights = step(lights)
        lights[0][0] = True
        lights[0][-1] = True
        lights[-1][0] = True
        lights[-1][-1] = True
    return sum(sum(row) for row in lights)
# end part2

if __name__ == '__main__':
    lights = get_input()
    print part1(lights)
    print part2(lights)

