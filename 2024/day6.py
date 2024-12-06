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
  size = (len(grid), len(grid[0]))
  pos = None
  obstacles = set()
  for y, row in enumerate(grid):
    for x, c in enumerate(row):
      if c == '^':
        pos = (y, x)
      elif c == '#':
        obstacles.add((y, x))
      else:
        assert c == '.'
  return size, pos, (-1, 0), obstacles


def part1(input):
  size, pos, delta, obstacles = input
  visited = set()
  while 0 <= pos[0] < size[0] and 0 <= pos[1] < size[1]:
    visited.add(pos)
    next = (pos[0] + delta[0], pos[1] + delta[1])
    while next in obstacles:
      delta = (delta[1], -delta[0])
      next = (pos[0] + delta[0], pos[1] + delta[1])
    pos = next
  return len(visited)


def part2(input):
  size, start_pos, start_delta, start_obstacles = input
  candidates = set()
  pos, delta = start_pos, start_delta
  while 0 <= pos[0] < size[0] and 0 <= pos[1] < size[1]:
    if pos != start_pos:
      candidates.add(pos)
    next = (pos[0] + delta[0], pos[1] + delta[1])
    while next in start_obstacles:
      delta = (delta[1], -delta[0])
      next = (pos[0] + delta[0], pos[1] + delta[1])
    pos = next

  count = 0
  for candidate in candidates:
    obstacles = set(start_obstacles)
    obstacles.add(candidate)
    pos, delta = start_pos, start_delta
    visited = set()
    while 0 <= pos[0] < size[0] and 0 <= pos[1] < size[1]:
      if (pos, delta) in visited:
        count += 1
        break
      else:
        visited.add((pos, delta))
      next = (pos[0] + delta[0], pos[1] + delta[1])
      while next in obstacles:
        delta = (delta[1], -delta[0])
        next = (pos[0] + delta[0], pos[1] + delta[1])
      pos = next

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
