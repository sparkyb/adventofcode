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

    return [line.split(' ') for line in input.split('\n')]
# end get_input

def resolve(registers, arg):
    if arg.isalpha():
        return registers[arg]
    else:
        return int(arg)

def executeasm(lines, defaults=None):
    registers = defaultdict(int)
    if defaults:
        registers.update(defaults)
    i = 0
    count = 0
    while i < len(lines):
        line = lines[i]
        op = line[0]
        args = line[1:]
        if op == 'set':
            registers[args[0]] = resolve(registers,args[1])
        elif op == 'sub':
            registers[args[0]] = registers[args[0]]-resolve(registers,args[1])
        elif op == 'mul':
            count += 1
            registers[args[0]] = registers[args[0]]*resolve(registers,args[1])
        elif op == 'jnz':
            if resolve(registers,args[0]) != 0:
                i = max(i+resolve(registers,args[1]),0)
                continue
        i += 1
    return count
# end executeasm

def part1(input):
    return executeasm(input)
# end part1

def part2(input):
    h=0
    for i in xrange(1001):
        b = 105700 + i*17
        for d in xrange(2,b):
            if b%d==0:
                h+=1
                break
    return h
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

