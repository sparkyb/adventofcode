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

    return dict((k,int(v)) for k,v in (re.search(r'^Generator ([A-Z]) starts with (\d+)$', line).groups() for line in input.split('\n')))
# end get_input

FACTORS = {'A': 16807, 'B': 48271}
DIVISOR = 2147483647

def generate_next(value, factor, multiple=1):
    while True:
        value = (value * factor) % DIVISOR
        if value % multiple == 0:
            return value
# end generate_next

def count_pairs(input, n, multiples = {'A':1, 'B':1}):
    values = dict(input)
    pairs = 0
    for i in xrange(n):
        for k,v in values.items():
            values[k] = generate_next(v,FACTORS[k],multiples[k])
        if (values['A']&0xFFFF) == (values['B']&0xFFFF):
            pairs += 1
    return pairs
# end count_pairs

def part1(input):
    return count_pairs(input, 40000000)
# end part1

def part2(input):
    return count_pairs(input, 5000000, {'A': 4, 'B': 8})
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)
