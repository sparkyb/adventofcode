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

  grid = input.split('\n')
  numbers = []
  symbols = {}
  for y, line in enumerate(grid):
    for match in re.finditer(r'\d+', line):
      num = int(match.group(0))
      numbers.append((y, match.span(), num))
    for x, symbol in enumerate(line):
      if symbol != '.' and not symbol.isdigit():
        symbols[(y, x)] = symbol
  return numbers, symbols



def part1(input):
  numbers, symbols = input
  total = 0
  for y, x, num in numbers:
    for y2 in range(y - 1, y + 2):
      for x2 in range(x[0] - 1, x[1] + 1):
        if (y2, x2) in symbols:
          total += num
          break
      else:
        continue
      break
  return total


def part2(input):
  numbers, symbols = input
  gears = collections.defaultdict(list)
  for y, x, num in numbers:
    for y2 in range(y - 1, y + 2):
      for x2 in range(x[0] - 1, x[1] + 1):
        if symbols.get((y2, x2)) == '*':
          gears[(y2, x2)].append(num)

  return sum(nums[0] * nums[1] for nums in gears.values() if len(nums) == 2)


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
