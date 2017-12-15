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

    return [re.search(r'(\w+) (inc|dec) (-?\d+) if (\w+) (>|<|==|!=|>=|<=) (-?\d+)', line).groups() for line in input.split('\n')]
# end get_input

def comp(a, op, b):
    if op == '==':
        return a == b
    elif op == '!=':
        return a != b
    elif op == '>':
        return a > b
    elif op == '<':
        return a < b
    elif op == '>=':
        return a >= b
    elif op == '<=':
        return a <= b
    else:
        raise ValueError("Unknown op: "+op)

def part1(input):
    registers = defaultdict(int)
    for r, dir, amount, r2, cond, amount2 in input:
        amount = int(amount)
        if dir == 'dec':
            amount = -amount
        amount2 = int(amount2)
        if comp(registers[r2], cond, amount2):
            registers[r] += amount
    return max(registers.values())
# end part1

def part2(input):
    m = None
    registers = defaultdict(int)
    for r, dir, amount, r2, cond, amount2 in input:
        amount = int(amount)
        if dir == 'dec':
            amount = -amount
        amount2 = int(amount2)
        if comp(registers[r2], cond, amount2):
            registers[r] += amount
            if (m is None or registers[r] > m):
                m = registers[r]
    return m
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

