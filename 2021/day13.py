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

  dot_lines, fold_lines = input.split('\n\n')
  dots = set(tuple(map(int, line.split(','))) for line in dot_lines.split('\n'))
  folds = []
  for line in fold_lines.split('\n'):
    axis, value = re.search(r'^fold along ([xy])=(\d+)$', line).groups()
    folds.append((axis, int(value)))
  return dots, folds


def fold(dots, axis, value):
  new_dots = set()
  for x, y in dots:
    if axis == 'x' and x > value:
      x = value - (x - value)
    elif axis == 'y' and y > value:
      y = value - (y - value)
    new_dots.add((x, y))
  return new_dots


def part1(input):
  dots, folds = input
  return len(fold(dots, *folds[0]))


def part2(input):
  dots, folds = input
  for axis, value in folds:
    dots = fold(dots, axis, value)
  for y in range(max(y for x, y in dots) + 1):
    for x in range(max(x for x, y in dots) + 1):
      print('#' if (x, y) in dots else ' ', end='')
    print()


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
