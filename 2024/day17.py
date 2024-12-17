#!/usr/bin/env python

import collections
from collections import defaultdict
import enum
import functools
import itertools
import math
import msvcrt
import operator
import os.path
import re
import sys

#import numpy as np


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  registers, opcodes = input.split('\n\n')
  registers = [int(re.search(r'^Register [ABC]: (\d+)$', line)[1])
               for line in registers.split('\n')]
  opcodes = [int(n)
             for n in re.search(r'^Program: ([0-9,]+)$', opcodes)[1].split(',')]
  return registers, opcodes


def combo(arg, registers):
  assert 0 <= arg < 7
  return registers[arg & 3] if arg & 4 else arg


def run_machine(registers, opcodes):
  registers = list(registers)
  output = []
  ip = 0
  while ip < len(opcodes):
    opcode = opcodes[ip]
    assert 0 <= opcode <= 7
    arg = opcodes[ip + 1]
    ip += 2
    if opcode == 0:
      registers[0] = registers[0] >> combo(arg, registers)
    elif opcode == 1:
      registers[1] ^= arg
    elif opcode == 2:
      registers[1] = combo(arg, registers) % 8
    elif opcode == 3:
      if registers[0]:
        ip = arg
    elif opcode == 4:
      registers[1] ^= registers[2]
    elif opcode == 5:
      output.append(combo(arg, registers) % 8)
    elif opcode == 6:
      registers[1] = registers[0] >> combo(arg, registers)
    elif opcode == 7:
      registers[2] = registers[0] >> combo(arg, registers)
  return output


def part1(input):
  registers, opcodes = input
  output = run_machine(registers, opcodes)
  return ','.join(str(n) for n in output)


def build_a(opcodes, a=0):
  if not opcodes:
    return a
  for next_nibble in range(1 if not a else 0, 8):
    next_a = (a << 3) | next_nibble
    b = next_nibble ^ 4
    c = next_a >> b
    b ^= c
    b ^= 4
    if b & 7 == opcodes[-1]:
      final_a = build_a(opcodes[:-1], next_a)
      if final_a:
        return final_a
  return None


def part2(input):
  registers, opcodes = input
  registers[0] = build_a(opcodes)
  assert run_machine(registers, opcodes) == opcodes
  return registers[0]


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('-c', '--clip', '--copy', action='store_true',
                      help='Copy answer to clipboard')
  parser.add_argument('-p', '--part', type=int, choices=(1, 2),
                      help='Which part to run (default: both)')
  parser.add_argument('-1', '--part1', action='store_const', dest='part',
                      const=1, help='Part 1 only')
  parser.add_argument('-2', '--part2', action='store_const', dest='part',
                      const=2, help='Part 2 only')
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  if args.clip:
    import pyperclip
  input = get_input(args.input)
  if not args.part or args.part == 1:
    answer1 = part1(input)
    print(answer1)
    if args.clip and answer1 is not None:
      pyperclip.copy(str(answer1))
  if not args.part or args.part == 2:
    answer2 = part2(input)
    print(answer2)
    if args.clip and answer2 is not None:
      pyperclip.copy(str(answer2))
