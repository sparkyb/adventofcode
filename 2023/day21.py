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
      if c != '#'
  }


def part1(input):
  plots = {(y, x) for (y, x), c in input.items() if c == 'S'}
  for _ in range(64):
    new_plots = set()
    for y, x in plots:
      for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        if (y + dy, x + dx) in input:
          new_plots.add((y + dy, x + dx))
    plots = new_plots
  return len(plots)


def simulate_block(input, plots):
  height = max(y for y, _ in input) + 1
  width = max(x for _, x in input) + 1
  prev_plots = frozenset()
  counts = []
  while plots:
    counts.append(len(plots) + (counts[-2] if len(counts) > 1 else 0))
    new_plots = frozenset(
        (y + dy, x + dx)
        for y, x in plots
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1))
        if (y + dy, x + dx) in input
        and (y + dy, x + dx) not in prev_plots
    )
    prev_plots = plots
    plots = new_plots
  return counts


def part2(input):
  height = max(y for y, _ in input) + 1
  width = max(x for _, x in input) + 1
  assert height == width
  side = height

  n = 26501365

  for (y, x), c in input.items():
    if c == 'S':
      cy = y
      cx = x
      break

  total = 0
  for sy in (-1, 0, 1):
    for sx in (-1, 0, 1):
      y = (height - 1, cy, 0)[sy + 1]
      x = (width - 1, cx, 0)[sx + 1]
      counts = simulate_block(input, {(y, x)})
      first_step = (cy + 1, 0, height - cy)[sy + 1] + (cx + 1, 0, width - cx)[sx + 1]
      steps = n - first_step
      if steps < 0:
        continue
      if sx == 0 and sy == 0:
        if steps < len(counts):
          c = counts[steps]
        else:
          c = counts[-2 + (steps - len(counts)) % 2]
        total += c
        continue
      level = steps // side
      for l in range(level + 1):
        s = steps - l * side
        if s < len(counts):
          c = counts[s]
        else:
          c = counts[-2 + (s - len(counts)) % 2]
        total += c * pow(l + 1, abs(sx) + abs(sy) - 1)
  return total


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
