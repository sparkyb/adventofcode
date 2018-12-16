import operator
import os.path
import re
import math
from collections import defaultdict
import itertools
import md5
import msvcrt
import sys


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0]+'.txt'
  with open(filename) as fp:
    input = fp.read().rstrip()

  samples = [map(int, sample) for sample in re.findall(r'^Before: \[(-?\d+), (-?\d+), (-?\d+), (-?\d+)\]\n(-?\d+) (-?\d+) (-?\d+) (-?\d+)\nAfter:  \[(-?\d+), (-?\d+), (-?\d+), (-?\d+)\]$',input,re.M)]
  samples = [{'before':sample[:4],'after':sample[-4:],'instruction':sample[4:8]} for sample in samples]
  instructions = [map(int, line.split(' ')) for line in re.sub(r'^Before: \[(-?\d+), (-?\d+), (-?\d+), (-?\d+)\]\n(-?\d+) (-?\d+) (-?\d+) (-?\d+)\nAfter:  \[(-?\d+), (-?\d+), (-?\d+), (-?\d+)\]$','',input,flags=re.M).strip().split('\n')]
  return samples, instructions

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

def executeasm(registers, instruction, opcode):
  registers[instruction[3]] = opcode['op'](opcode['a'](registers,instruction[1]),opcode['b'](registers,instruction[2]))
  return registers

def valid_opcodes(sample):
  opcodes = set()
  for key,opcode in OPCODES.items():
    registers = list(sample['before'])
    if executeasm(list(sample['before']), sample['instruction'], opcode) == sample['after']:
      opcodes.add(key)
  return opcodes

def part1(input):
  samples, instructions = input
  count = 0
  for sample in samples:
    if len(valid_opcodes(sample)) >= 3:
      count += 1
  return count

def part2(input):
  samples, instructions = input
  opcodes = [set(OPCODES.keys()) for i in xrange(16)]
  for sample in samples:
    num = sample['instruction'][0]
    opcodes[num] &= valid_opcodes(sample)
    if len(opcodes[num]) == 1:
      for i in xrange(len(opcodes)):
        if i == num: continue
        opcodes[i] -= opcodes[num]
  assert all(len(ops) == 1 for ops in opcodes)
  opcodes = [list(ops)[0] for ops in opcodes]

  registers = [0, 0, 0, 0]
  for instruction in instructions:
    executeasm(registers, instruction, OPCODES[opcodes[instruction[0]]])
  return registers[0]


if __name__ == '__main__':
  input = get_input()
  print part1(input)
  print part2(input)
