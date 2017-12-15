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

    return map(int, re.split(r'\s+', input))
# end get_input

def highest(blocks):
    return blocks.index(max(blocks))

def redistribute(blocks):
    blocks = list(blocks)
    i = highest(blocks)
    n = blocks[i]
    blocks[i] = 0
    for j in xrange(n):
        blocks[(i+j+1)%len(blocks)] += 1
    return blocks
    

def part1(blocks):
    seen = set([tuple(blocks)])
    step = 0
    while True:
        blocks = tuple(redistribute(blocks))
        step += 1
        if blocks in seen:
            return step
        seen.add(blocks)
# end part1

def part2(blocks):
    seen = {tuple(blocks):0}
    step = 0
    while True:
        blocks = tuple(redistribute(blocks))
        step += 1
        if blocks in seen:
            return step-seen[blocks]
        seen[blocks]=step
# end part2

if __name__ == '__main__':
    blocks = get_input()
    print part1(blocks)
    print part2(blocks)

