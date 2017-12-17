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

    return int(input)
# end get_input

def part1(input):
    buffer = [0]
    index = 0
    for i in xrange(1, 2018):
        index = (index + input) % len(buffer) + 1
        buffer.insert(index, i)
    return buffer[(index+1)%len(buffer)]
# end part1

def part2(input):
    value = 0
    index = 0
    for i in xrange(1, 50000001):
        index = (index + input) % i + 1
        if index == 1:
            value = i
    return value
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

