import re
from collections import defaultdict


def get_input():
    with open('day12.txt') as fp:
        input = fp.read().strip()
    
    return [line.split() for line in input.split('\n')]
# end get_input

def executeasm(lines, defaults=None):
    registers = defaultdict(int)
    if defaults:
        registers.update(defaults)
    i = 0
    while i < len(lines):
        line = lines[i]
        op = line[0]
        args = line[1:]
        if op == 'cpy':
            if args[0].isalpha():
                registers[args[1]] = registers[args[0]]
            else:
                registers[args[1]] = int(args[0])
        elif op == 'inc':
            registers[args[0]] += 1
        elif op == 'dec':
            registers[args[0]] -= 1
        elif op == 'jnz':
            if args[0].isalpha():
                if registers[args[0]]:
                    i += int(args[1])
                    continue
            else:
                if int(args[0]):
                    i += int(args[1])
                    continue
        i += 1
    return registers
# end executeasm
    
def part1(lines):
    return executeasm(lines)['a']
# end part1

def part2(lines):
    return executeasm(lines,{'c':1})['a']
# end part2

if __name__ == '__main__':
    lines = get_input()
    print part1(lines)
    print part2(lines)

