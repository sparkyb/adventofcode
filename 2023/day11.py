#!/usr/bin/env python

import bisect
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

  return {(y, x) for y, line in enumerate(input.split('\n'))
          for x, c in enumerate(line) if c == '#'}


def expand(galaxies, amount=2):
  max_y = max(y for y, _ in galaxies)
  max_x = max(x for _, x in galaxies)
  empty_rows = []
  empty_cols = []
  for y in range(max_y):
    if not any(y2 == y for y2, _ in galaxies):
      empty_rows.append(y)
  for x in range(max_x):
    if not any(x2 == x for _, x2 in galaxies):
      empty_cols.append(x)

  return {(y + bisect.bisect(empty_rows, y) * (amount - 1),
           x + bisect.bisect(empty_cols, x) * (amount - 1))
          for y, x in galaxies}

def part1(input):
  galaxies = expand(input)
  return sum(abs(y2 - y1) + abs(x2 - x1)
             for (y1, x1), (y2, x2) in itertools.combinations(galaxies, 2))


def part2(input):
  galaxies = expand(input, amount=1000000)
  return sum(abs(y2 - y1) + abs(x2 - x1)
             for (y1, x1), (y2, x2) in itertools.combinations(galaxies, 2))


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
