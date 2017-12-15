import re
from collections import defaultdict


def get_input():
    with open('day25.txt') as fp:
        input = fp.read().strip()
    
    return [line.split() for line in input.split('\n')]
# end get_input

def resolve(registers, arg):
    if arg.isalpha():
        return registers[arg]
    else:
        return int(arg)

def executeasm(lines, defaults=None, i=0):
    registers = defaultdict(int)
    if defaults:
        registers.update(defaults)
    lines = [list(line) for line in lines]
    while i < len(lines):
        line = lines[i]
        ## print i, ' '.join(line)
        ## raw_input()
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
        elif op == 'out':
            yield resolve(registers,args[0]),registers,i
        else:
            raise ValueError('Unknown op: '+' '.join(line))
        i += 1
# end executeasm

def part1(lines):
    a = 0
    while True:
        print a
        buffer = []
        for b, registers, i in executeasm(lines, {'a':a}, 0):
            if b != len(buffer)%2:
                break
            registers = tuple(registers[x] for x in 'abcd')
            if (b,registers,i) in buffer:
                return a
            buffer.append((b,registers,i))
        a += 1
# end part1

if __name__ == '__main__':
    lines = get_input()
    print part1(lines)

