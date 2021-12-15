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

  return {(y, x): int(c) for y, line in enumerate(input.split('\n')) for x, c in enumerate(line)}


def neighbors(y, x):
  yield (y - 1, x)
  yield (y + 1, x)
  yield (y, x - 1)
  yield (y, x + 1)


def get_size(risk):
  return (max(y for y, _ in risk) + 1, max(x for _, x in risk) + 1)


def get_risk(size, risk, y, x, tile=1):
  ty = y // size[0]
  tx = x // size[1]
  if ty < 0 or ty >= tile or tx < 0 or tx >= tile:
    return None
  y %= size[0]
  x %= size[1]
  return (risk[(y, x)] + tx + ty - 1) % 9 + 1


def min_path(risk, tile=1):
  size = get_size(risk)
  visited = {(0, 0)}
  frontier = [(0, (0, 0))]
  while frontier:
    r, (y, x) = heapq.heappop(frontier)
    for y2, x2 in neighbors(y, x):
      if (y2, x2) in visited:
        continue
      r2 = get_risk(size, risk, y2, x2, tile=tile)
      if r2 is None:
        continue
      r2 += r
      if y2 == size[0] * tile - 1 and x2 == size[1] * tile - 1:
        return r2
      visited.add((y2, x2))
      heapq.heappush(frontier, (r2, (y2, x2)))


def part1(risk):
  return min_path(risk)


def part2(risk):
  return min_path(risk, tile=5)


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
