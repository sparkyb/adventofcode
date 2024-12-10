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

  heights = {(y, x): int(c) for y, row in enumerate(input.split('\n'))
             for x, c in enumerate(row)}
  trailheads = {pos for pos, height in heights.items() if height == 0}
  return heights, trailheads


def part1(input):
  heights, trailheads = input
  score = 0
  for start in trailheads:
    frontier = {start}
    ends = set()
    while frontier:
      pos = frontier.pop()
      val = heights[pos]
      if val == 9:
        ends.add(pos)
      else:
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
          pos2 = (pos[0] + dy, pos[1] + dx)
          if heights.get(pos2, -1) == val + 1:
            frontier.add(pos2)
    score += len(ends)
  return score


def part2(input):
  heights, trailheads = input
  score = 0
  for start in trailheads:
    frontier = {(start,)}
    ends = set()
    while frontier:
      path = frontier.pop()
      pos = path[-1]
      val = heights[pos]
      if val == 9:
        score += 1
      else:
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
          pos2 = (pos[0] + dy, pos[1] + dx)
          if heights.get(pos2, -1) == val + 1:
            frontier.add(path + (pos2,))
  return score


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
