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

    return map(int, re.search(r'row (\d+), column (\d+).', input).groups())
# end get_input

def part1(row, col):
    row -= 1
    col -= 1
    n = row + col
    index = n*(n+1)/2 + col
    n = 20151125
    print index
    for i in xrange(index):
        n = (n*252533)%33554393
    return n
    #return (20151125*pow(252533,index)) % 33554393
# end part1

def part2(row, col):
    return None
# end part2

if __name__ == '__main__':
    row, col = get_input()
    print part1(row, col)
    print part2(row, col)

