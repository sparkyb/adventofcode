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
    snd = []
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
            val = yield resolve(registers,args[0])
            if val is not None:
                snd.append(val)
        elif op == 'rcv':
            if snd:
                registers[args[0]] = snd.pop(0)
            else:
                val = yield None
                while val is None:
                    val = yield None
                registers[args[0]] = val
        i += 1
# end executeasm

def part2(input):
    prog0 = executeasm(input, {'p':0})
    prog1 = executeasm(input, {'p':1})
    prog0q = [None]
    prog1q = [None]
    prog0locked = False
    prog1locked = False
    count = 0
    while not prog0locked or not prog0locked or prog0q or prog1q:
        while prog1q or not prog0locked:
            val = prog0.send(prog1q.pop(0) if prog1q else None)
            #print 'prog0 yielded %s' % val
            if val is not None:
                prog0locked = False
                prog0q.append(val)
            else:
                prog0locked = True
        while prog0q or not prog1locked:
            val = prog1.send(prog0q.pop(0) if prog0q else None)
            #print 'prog1 yielded %s' % val
            if val is not None:
                prog1locked = False
                prog1q.append(val)
                count += 1
            else:
                prog1locked = True
    return count
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

