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

  return [line.split(' = ') for line in input.split('\n')]


def part1(input):
  mem = {}
  masks = [0, 0]
  for l, r in input:
    if l == 'mask':
      masks = [0, 0]
      for bit, val in enumerate(reversed(r)):
        if val != 'X':
          masks[int(val)] |= pow(2, bit)
    else:
      addr = int(re.search('^mem\[(\d+)\]$', l).group(1))
      mem[addr] = (int(r) | masks[1]) & ~masks[0]
  return sum(mem.values())


def mask_addrs(masks, addr):
  addr |= masks[1]
  addr &= ~masks[0]
  mask_bits = [1 << bit for bit in range(36) if (masks[0] >> bit) & 1]
  for r in range( len(mask_bits) + 1):
    for one_bits in itertools.combinations(mask_bits, r):
      yield functools.reduce(operator.or_, one_bits, addr)


def part2(input):
  mem = {}
  masks = [0, 0]
  for l, r in input:
    if l == 'mask':
      masks = [0, 0]
      for bit, val in enumerate(reversed(r)):
        if val == '1':
          masks[1] |= pow(2, bit)
        elif val == 'X':
          masks[0] |= pow(2, bit)
    else:
      val = int(r)
      for addr in mask_addrs(masks,
                             int(re.search('^mem\[(\d+)\]$', l).group(1))):
        mem[addr] = val
  return sum(mem.values())


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
