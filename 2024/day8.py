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
  freqs = collections.defaultdict(set)
  for y, row in enumerate(grid):
    for x, c in enumerate(row):
      if c != '.':
        freqs[c].add((y, x))
  return size, freqs


def part1(input):
  size, freqs = input
  antinodes = set()
  for nodes in freqs.values():
    for a, b in itertools.combinations(nodes, 2):
      dy = b[0] - a[0]
      dx = b[1] - a[1]
      y, x = a[0] - dy, a[1] - dx
      if 0 <= y < size[0] and 0 <= x < size[1]:
        antinodes.add((y, x))
      y, x = b[0] + dy, b[1] + dx
      if 0 <= y < size[0] and 0 <= x < size[1]:
        antinodes.add((y, x))
  return len(antinodes)


def part2(input):
  size, freqs = input
  antinodes = set()
  for nodes in freqs.values():
    for a, b in itertools.combinations(nodes, 2):
      dy = b[0] - a[0]
      dx = b[1] - a[1]
      y, x = a
      while 0 <= y < size[0] and 0 <= x < size[1]:
        antinodes.add((y, x))
        y -= dy
        x -= dx
      y, x = b
      while 0 <= y < size[0] and 0 <= x < size[1]:
        antinodes.add((y, x))
        y += dy
        x += dx
  return len(antinodes)


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
