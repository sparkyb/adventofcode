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

  return [[c for c in line] for line in input.split('\n')]


def part1(input, start=((0, 0), (0, 1))):
  visited = set()
  queue = [start]
  while queue:
    (y, x), (dy, dx) = queue.pop()
    if y < 0 or y >= len(input) or x < 0 or x >= len(input[y]):
      continue
    key = ((y, x), (dy, dx))
    if key in visited:
      continue
    visited.add(key)
    tile = input[y][x]
    if tile == '.' or (tile == '-' and dx) or (tile == '|' and dy):
      queue.append(((y + dy, x + dx), (dy, dx)))
    elif tile == '/':
      queue.append(((y - dx, x - dy), (-dx, -dy)))
    elif tile == '\\':
      queue.append(((y + dx, x + dy), (dx, dy)))
    elif tile == '-':
      queue.append(((y, x - 1), (0, -1)))
      queue.append(((y, x + 1), (0, 1)))
    elif tile == '|':
      queue.append(((y - 1, x), (-1, 0)))
      queue.append(((y + 1, x), (1, 0)))
    else:
      raise ValueError
  return len({pos for pos, _ in visited})


def part2(input):
  max_energized = 0
  for y in range(len(input)):
    max_energized = max(max_energized, part1(input, ((y, 0), (0, 1))))
    max_energized = max(max_energized,
                        part1(input, ((y, len(input[y]) - 1), (0, -1))))
  for x in range(len(input[0])):
    max_energized = max(max_energized, part1(input, ((0, x), (1, 0))))
    max_energized = max(max_energized,
                        part1(input, ((len(input) - 1, x), (-1, 0))))
  return max_energized


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
