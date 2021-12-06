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

  return [list(map(int,
                   re.search(r'^(\d+),(\d+) -> (\d+),(\d+)$', line).groups()))
          for line in input.split('\n')]


def sign(n):
  return (n > 0) - (n < 0)


def to_points(x1, y1, x2, y2):
  return set((x1 + i * sign(x2 - x1), y1 + i * sign(y2 - y1))
             for i in range(max(abs(x2 - x1), abs(y2 - y1)) + 1))


def part1(input):
  filled = collections.Counter()
  for x1, y1, x2, y2 in input:
    if x1 == x2 or y1 == y2:
      filled.update(to_points(x1, y1, x2, y2))
  return sum(1 for count in filled.values() if count > 1)


def part2(input):
  filled = collections.Counter()
  for x1, y1, x2, y2 in input:
    filled.update(to_points(x1, y1, x2, y2))
  return sum(1 for count in filled.values() if count > 1)


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
