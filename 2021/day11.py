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

  return {(y, x): int(c) for y, row in enumerate(input.split('\n')) for x, c in enumerate(row)}


def step(grid):
  flashes = 0
  q = collections.deque()
  for y, x in grid:
    grid[y, x] += 1
    if grid[y, x] > 9:
      grid[y, x] = 0
      q.append((y, x))
  while q:
    y, x = q.pop()
    flashes += 1
    for y2, x2 in itertools.product((y - 1, y, y + 1), (x - 1, x, x + 1)):
      if y2 == y and x2 == x:
        continue
      if not grid.get((y2, x2), 0):
        continue
      grid[y2, x2] += 1
      if grid[y2, x2] > 9:
        grid[y2, x2] = 0
        q.append((y2, x2))
  return flashes


def part1(input):
  grid = dict(input)
  flashes = 0
  for i in range(100):
    flashes += step(grid)
  return flashes


def part2(input):
  grid = dict(input)
  flashes = 0
  for i in itertools.count(1):
    flashes = step(grid)
    if flashes == 100:
      return i


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
