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

def part1(lines):
    registers = defaultdict(int)
    i = 0
    snd = None
    while i < len(lines):
        line = lines[i]
        op = line[0]
        args = line[1:]
        if op == 'set':
            registers[args[0]] = resolve(registers,args[1])
        elif op == 'add':
            registers[args[0]] = registers[args[0]]+resolve(registers,args[1])
        elif op == 'mul':
            registers[args[0]] = registers[args[0]]*resolve(registers,args[1])
        elif op == 'mod':
            registers[args[0]] = registers[args[0]]%resolve(registers,args[1])
        elif op == 'jgz':
            if resolve(registers,args[0]) > 0:
                i = max(i+resolve(registers,args[1]),0)
                continue
        elif op == 'snd':
            snd = resolve(registers,args[0])
        elif op == 'rcv':
            if resolve(registers,args[0]) != 0:
                return snd
        i += 1
# end part1

def executeasm(lines, defaults=None):
    registers = defaultdict(int)
    if defaults:
        registers.update(defaults)
    i = 0
    inqueue = []
    outqueue = []
    while i < len(lines):
        line = lines[i]
        op = line[0]
        args = line[1:]
        if op == 'set':
            registers[args[0]] = resolve(registers,args[1])
        elif op == 'add':
            registers[args[0]] = registers[args[0]]+resolve(registers,args[1])
        elif op == 'mul':
            registers[args[0]] = registers[args[0]]*resolve(registers,args[1])
        elif op == 'mod':
            registers[args[0]] = registers[args[0]]%resolve(registers,args[1])
        elif op == 'jgz':
            if resolve(registers,args[0]) > 0:
                i = max(i+resolve(registers,args[1]),0)
                continue
        elif op == 'snd':
            outqueue.append(resolve(registers,args[0]))
        elif op == 'rcv':
            while not inqueue:
                inqueue = yield outqueue
                outqueue = []
            registers[args[0]] = inqueue.pop(0)
        i += 1
# end executeasm

def part2(input):
    prog0 = executeasm(input, {'p':0})
    prog1 = executeasm(input, {'p':1})
    prog0q = prog0.next()
    prog1q = prog1.next()
    count = 0
    while prog0q or prog1q:
        if prog1q:
            prog0q.extend(prog0.send(prog1q))
            prog1q = []
        if prog0q:
            vals = prog1.send(prog0q)
            count += len(vals)
            prog1q.extend(vals)
            prog0q = []
    return count
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

