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

  return [[tuple(map(int, point.split(','))) for point in line.split(' -> ')]
          for line in input.split('\n')]


def sign(x):
  return (x > 0) - (x < 0)


def fill_grid(lines):
  grid = {}
  for line in lines:
    for i in range(len(line) - 1):
      x, y = line[i]
      x2, y2 = line[i + 1]
      dx, dy = sign(x2 - x), sign(y2 - y)
      while x != x2 or y != y2:
        grid[(x, y)] = '#'
        x += dx
        y += dy
      grid[(x, y)] = '#'
  return grid


def fall_sand(grid, start=(500, 0), floor=None):
  max_y = max(y for _, y in grid.keys())
  if floor is not None:
    max_y += floor
  sand = 0
  x, y = start
  while y < max_y:
    for below in [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]:
      if below not in grid and (floor is None or below[1] < max_y):
        x, y = below
        break
    else:
      grid[(x, y)] = 'o'
      sand += 1
      if (x, y) == start:
        return sand
      x, y = start
  return sand


def draw_grid(grid):
  min_x = min(x for x, _ in grid.keys())
  max_x = max(x for x, _ in grid.keys())
  min_y = min(y for _, y in grid.keys())
  max_y = max(y for _, y in grid.keys())
  for y in range(min_y, max_y + 1):
    print(''.join(grid.get((x, y), '.') for x in range(min_x, max_x + 1)))


def part1(input):
  grid = fill_grid(input)
  return fall_sand(grid)


def part2(input):
  grid = fill_grid(input)
  return fall_sand(grid, floor=2)


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
