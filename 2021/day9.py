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

  return {(y, x): int(height)
          for y, line in enumerate(input.split('\n'))
          for x, height in enumerate(line)}


def neighbors(y, x):
  return ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1))


def low_points(input):
  for (y, x), height in input.items():
    for y2, x2 in neighbors(y, x):
      if input.get((y2, x2), 10) <= height:
        break
    else:
      yield y, x


def basin_size(input, y, x):
  q = collections.deque()
  basin = set()
  q.append((y, x))
  while q:
    y, x = q.pop()
    if (y, x) in basin:
      continue
    basin.add((y, x))
    for y2, x2 in neighbors(y, x):
      if input.get((y2, x2), 10) < 9 and (y2, x2) not in basin:
        q.append((y2, x2))
  return len(basin)


def part1(input):
  return sum(input[(y, x)] + 1 for y, x in low_points(input))


def part2(input):
  basin_sizes = [basin_size(input, y, x) for y, x in low_points(input)]
  basin_sizes.sort(reverse=True)
  return functools.reduce(operator.mul, basin_sizes[:3])


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
