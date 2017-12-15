import re
from collections import defaultdict


def get_input():
    with open('day23.txt') as fp:
        input = fp.read().strip()
    
    return [line.split() for line in input.split('\n')]
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
    lines = [list(line) for line in lines]
    while i < len(lines):
        line = lines[i]
        op = line[0]
        args = line[1:]
        if op == 'cpy':
            if args[1].isalpha():
                registers[args[1]] = resolve(registers,args[0])
        elif op == 'inc':
            if args[0].isalpha():
                registers[args[0]] += 1
        elif op == 'dec':
            if args[0].isalpha():
                registers[args[0]] -= 1
        elif op == 'jnz':
            if resolve(registers,args[0]):
                i = max(i+resolve(registers,args[1]),0)
                continue
        elif op == 'tgl':
            j = i+resolve(registers,args[0])
            if j >= 0 and j < len(lines):
                if (len(lines[j]) == 2):
                    if lines[j][0] == 'inc':
                        lines[j][0] = 'dec'
                    else:
                        lines[j][0] = 'inc'
                else:
                    if lines[j][0] == 'jnz':
                        lines[j][0] = 'cpy'
                    else:
                        lines[j][0] = 'jnz'
        i += 1
    return registers
# end executeasm

def part1(lines):
    return executeasm(lines,{'a':7})['a']
# end part1

def part2(lines):
    a=12
    b=a-1
    while b>1:
        a*=b
        b-=1
    a+=93*81
    return a
    return executeasm(lines,{'a':12})['a']
# end part2

if __name__ == '__main__':
    lines = get_input()
    print part1(lines)
    print part2(lines)

