import os.path
import re
import math
from collections import defaultdict
import itertools
import md5
import msvcrt
import sys
import operator


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
    opcode = OPCODES[instruction[0]]
    registers[instruction[3]] = opcode['op'](opcode['a'](registers,instruction[1]),opcode['b'](registers,instruction[2]))
    registers[ip] += 1
  return registers[0]

def decompiled(registers = None):
  if not registers:
    registers = defaultdict(int)

  registers[4] = pow(registers[4] + 2, 2) * 19 * 11
  registers[3] = (registers[3] + 2) * 22 + 13
  registers[4] += registers[3]
  if registers[0]:
    registers[3] = (27 * 28 + 29) * 30 * 14 * 32
    registers[4] += registers[3]

  for registers[2] in xrange(1, registers[4] + 1):
    ## for registers[1] in xrange(1, registers[4] + 1):
      ## if registers[2] * registers[1] == registers[4]:
        ## registers[0] += registers[2]
    if registers[4] % registers[2] == 0:
      registers[0] += registers[2]
  return registers[0]

def part1(input):
  ip, instructions = input
  registers = defaultdict(int)
  return executeasm(ip, instructions, registers)
  ## return decompiled(registers)

def part2(input):
  ip, instructions = input
  registers = defaultdict(int)
  registers[0] = 1  # part 2
  ## return executeasm(ip, instructions, registers)
  return decompiled(registers)


if __name__ == '__main__':
  input = get_input()
  print part1(input)
  print part2(input)
