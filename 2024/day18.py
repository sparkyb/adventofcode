#!/usr/bin/env python

import collections
from collections import defaultdict
import enum
import functools
import heapq
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

  return [tuple(int(n) for n in line.split(',')) for line in input.split('\n')]


def min_distance(corrupted):
  start = (0, 0)
  end = (70, 70)
  frontier = [(0, start)]
  scores = {}
  while frontier:
    score, pos = heapq.heappop(frontier)
    if pos == end:
      return score
    for dir in ((-1, 0), (1, 0), (0, -1), (0, 1)):
      next_pos = (pos[0] + dir[0], pos[1] + dir[1])
      if all(0 <= n <= 70 for n in next_pos) and next_pos not in corrupted:
        next_score = score + 1
        if next_pos not in scores or scores[next_pos] > next_score:
          scores[next_pos] = next_score
          heapq.heappush(frontier, (next_score, next_pos))
  return None


def part1(input):
  return min_distance(input[:1024])


def part2(input):
  l = 1025
  r = len(input) - 1
  while l != r:
    mid = l + (r - l) // 2
    if min_distance(input[:mid]) is None:
      r = mid
    else:
      l = mid + 1
  return ','.join(str(n) for n in input[l - 1])


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
