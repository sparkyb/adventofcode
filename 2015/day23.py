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

    return [(op,re.split(r',\s*', args)) for op,args in (line.split(None, 1) for line in input.split('\n'))]
# end get_input

def executeasm(lines, defaults=None):
    registers = defaultdict(int)
    if defaults:
        registers.update(defaults)
    i = 0
    while 0 <= i < len(lines):
        op, args = lines[i]
        ## print i+1, op, args, registers
        ## raw_input()
        if op == 'hlf':
            registers[args[0]] /= 2
        elif op == 'tpl':
            registers[args[0]] *= 3
        elif op == 'inc':
            registers[args[0]] += 1
        elif op == 'jmp':
            i += int(args[0])
            continue
        elif op == 'jie':
            if registers[args[0]] % 2 == 0:
                i += int(args[1])
                continue
        elif op == 'jio':
            if registers[args[0]] == 1:
                i += int(args[1])
                continue
        i += 1
    return registers
# end executeasm

def part1(lines):
    return executeasm(lines)['b']
# end part1

def part2(lines):
    return executeasm(lines, {'a':1})['b']
# end part2

if __name__ == '__main__':
    lines = get_input()
    print part1(lines)
    print part2(lines)

