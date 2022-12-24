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

  
  return {
      (y, x): c
      for y, line in enumerate(input.split('\n'))
      for x, c in enumerate(line)
      if c != '.'
  }


DIRECTIONS = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1),
    '#': (0, 0),
}


def on_step(grid, step):
  height = max(y for y, _ in grid) - 1
  width = max(x for _, x in grid) - 1
  new_grid = {}
  for (y, x), d in grid.items():
    dy, dx = DIRECTIONS[d]
    if dy or dx:
      y = (y + dy * step - 1) % height + 1
      x = (x + dx * step - 1) % width + 1
    if (y, x) in new_grid:
      if not isinstance(new_grid[(y, x)], int):
        new_grid[(y, x)] = 1
      new_grid[(y, x)] += 1
    else:
      new_grid[(y, x)] = d
  return new_grid


def draw_grid(grid):
  max_y = max(y for y, _ in input)
  max_x = max(x for _, x in input)
  for y in range(max_y + 1):
    print(''.join(str(grid.get((y, x), '.')) for x in range(max_x + 1)))
  print()


def lcm(*nums):
  return functools.reduce(lambda n, lcm: lcm * n // math.gcd(lcm, n), nums)


def find_target(grid, start, end, start_step=0):
  max_y = max(y for y, _ in grid)
  max_x = max(x for _, x in grid)
  cycle = lcm(max_y - 1, max_x - 1)
  steps = [on_step(grid, step) for step in range(cycle)]
  visited = set()
  frontier = collections.deque([(start, start_step)])
  while frontier:
    (y, x), step = frontier.popleft()
    if (y, x) == end:
      return step
    if ((y, x), step % cycle) in visited:
      continue
    visited.add(((y, x), step % cycle))
    next_step = (step + 1) % cycle
    next_grid = steps[next_step]
    for dy, dx in [(1, 0), (0, 1), (0, 0), (0, -1), (-1, 0)]:
      y2 = y + dy
      x2 = x + dx
      if 0 <= y2 <= max_y and (y2, x2) not in next_grid:
        frontier.append(((y2, x2), step + 1))
  return None


def part1(input):
  max_y = max(y for y, _ in input)
  max_x = max(x for _, x in input)
  start = (0, 1)
  end = (max_y, max_x - 1)
  return find_target(input, start, end)


def part2(input):
  max_y = max(y for y, _ in input)
  max_x = max(x for _, x in input)
  start = (0, 1)
  end = (max_y, max_x - 1)
  step = find_target(input, start, end)
  ## print(step)
  step = find_target(input, end, start, step)
  ## print(step)
  return find_target(input, start, end, step)


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
