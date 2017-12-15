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

    return dict(map(int, line.split(': ')) for line in input.split('\n'))
# end get_input

def scanner(input, depth, time):
    if depth not in input:
        return None
    range = input[depth]
    pos = time % (range * 2 - 2)
    if pos >= range:
        pos = 2 * range - pos - 2
    return pos

def part1(input, delay=0):
    score = 0
    for depth in sorted(input.keys()):
        #print depth, scanner(input, depth, depth), input[depth], scanner(input, depth, depth) == 0
        if scanner(input, depth, depth+delay) == 0:
            score += depth * input[depth]
    return score
# end part1

def part2(input):
    delay = 0
    while True:
        if scanner(input, 0, delay) != 0 and part1(input, delay) == 0:
            return delay
        delay += 1
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

