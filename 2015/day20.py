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

    return int(input)
# end get_input

def part1(n):
    houses = [10]*(n/10)
    for i in xrange(2,len(houses)):
        for h in xrange(i,len(houses),i):
            houses[h]+=i*10
        if houses[i] >= n:
            return i
# end part1

def part2(n):
    houses = defaultdict(int)
    i = 1
    while True:
        for j in xrange(i,i+i*50,i):
            houses[j]+=i*11
        if houses[i] >= n:
            return i
        i += 1
# end part2

if __name__ == '__main__':
    n = get_input()
    print part1(n)
    print part2(n)

