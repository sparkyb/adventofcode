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

  return input.split('\n')


def part1(input):
  lines = list(input)
  lines.extend(''.join(line) for line in zip(*input))
  width = len(input[0])
  height = len(input)
  for y in range(height):
    lines.append(''.join(input[y + x][x]
                         for x in range(min(height - y, width))))
    lines.append(''.join(input[y - x][x]
                         for x in range(min(y + 1, width))))
  for x in range(1, width):
    lines.append(''.join(input[y][x + y]
                         for y in range(min(width - x, height))))
    lines.append(''.join(input[height - y - 1][x + y]
                         for y in range(min(width - x, height))))
  lines.extend([''.join(reversed(line)) for line in lines])
  return sum(len(re.findall(r'XMAS', line)) for line in lines)


def part2(input):
  mas = set('MAS')
  width = len(input[0])
  height = len(input)
  count = 0
  for y in range(1, height - 1):
    for x in range(1, width - 1):
      if input[y][x] == 'A':
        diag1 = set(input[y + i][x + i] for i in range(-1, 2))
        diag2 = set(input[y + i][x - i] for i in range(-1, 2))
        if diag1 == diag2 == mas:
          count += 1
  return count


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
