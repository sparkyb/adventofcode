import os.path
import re
import math
from collections import defaultdict
import itertools
import md5
import msvcrt
import operator
import sys


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0]+'.txt'
  with open(filename) as fp:
    input = fp.read().rstrip()

  lines = input.split('\n')
  ip = int(re.search(r'^#ip (\d)$', lines[0]).group(1))
  return ip, [(opcode, int(a), int(b), int(c)) for opcode, a, b, c in [line.split(' ') for line in lines[1:]]]


def register(registers, value):
  return registers[value]

def immediate(registers, value):
  return value

OPCODES = {
  'addr': {'op':operator.add,'a':register,'b':register},
  'addi': {'op':operator.add,'a':register,'b':immediate},
  'mulr': {'op':operator.mul,'a':register,'b':register},
  'muli': {'op':operator.mul,'a':register,'b':immediate},
  'banr': {'op':operator.and_,'a':register,'b':register},
  'bani': {'op':operator.and_,'a':register,'b':immediate},
  'borr': {'op':operator.or_,'a':register,'b':register},
  'bori': {'op':operator.or_,'a':register,'b':immediate},
  'setr': {'op':(lambda a,b: a),'a':register,'b':immediate},
  'seti': {'op':(lambda a,b: a),'a':immediate,'b':immediate},
  'gtir': {'op':operator.gt,'a':immediate,'b':register},
  'gtri': {'op':operator.gt,'a':register,'b':immediate},
  'gtrr': {'op':operator.gt,'a':register,'b':register},
  'eqir': {'op':operator.eq,'a':immediate,'b':register},
  'eqri': {'op':operator.eq,'a':register,'b':immediate},
  'eqrr': {'op':operator.eq,'a':register,'b':register},
}

def executeasm(ip, instructions, registers = None):
  if not registers:
    registers = defaultdict(int)
  while registers[ip] >= 0 and registers[ip] < len(instructions):
    instruction = instructions[registers[ip]]
    ## print '%d: %s\t%r' %(registers[ip], ' '.join(map(str,instruction)), [registers[i] for i in xrange(6)])
    opcode = OPCODES[instruction[0]]
    registers[instruction[3]] = opcode['op'](opcode['a'](registers,instruction[1]),opcode['b'](registers,instruction[2]))
    registers[ip] += 1
  return registers[0]

def part1(input):
  r5 = 0
  while True:
    r4 = r5 | 0x10000
    r5 = 3935295
    while r4:
      r4, r2 = divmod(r4, 256)
      r5 += r2
      r5 &= 0xffffff
      r5 *= 65899
      r5 &= 0xffffff
    return r5

def part2(input):
  r5s = []
  r5 = 0
  while True:
    r4 = r5 | 0x10000
    r5 = 3935295
    while r4:
      r4, r2 = divmod(r4, 256)
      r5 += r2
      r5 &= 0xffffff
      r5 *= 65899
      r5 &= 0xffffff
    if r5 in r5s:
      return r5s[-1]
    else:
      ## print r5
      r5s.append(r5)
  

if __name__ == '__main__':
  input = get_input()
  print part1(input)
  print part2(input)
