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

  return [list(map(int, line)) for line in input.split('\n')]


def find_taller_neighbor(grid, y, x, dy, dx):
  height = len(grid)
  width = len(grid[0])
  y2 = y + dy
  x2 = x + dx
  while 0 <= y2 < height and 0 <= x2 < width:
    if grid[y2][x2] >= grid[y][x]:
      return False, abs(y2 - y) + abs(x2 - x)
    y2 += dy
    x2 += dx
  return True, abs(y2 - y) + abs(x2 - x) - 1


def visible_from_edge(grid, y, x):
  for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    if find_taller_neighbor(grid, y, x, dy, dx)[0]:
      return True
  return False


def distance_to_taller_neighbor(grid, y, x, dy, dx):
  return find_taller_neighbor(grid, y, x, dy, dx)[1]


def scenic_score(grid, y, x):
  return math.prod(distance_to_taller_neighbor(grid, y, x, dy, dx)
                   for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)])


def part1(input):
  height = len(input)
  width = len(input[0])
  return sum(visible_from_edge(input, y, x)
             for y in range(height) for x in range(width))


def part2(input):
  height = len(input)
  width = len(input[0])
  return max(scenic_score(input, y, x)
             for y in range(height) for x in range(width))


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
