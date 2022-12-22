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

  map, path = input.split('\n\n')
  map = {(y, x): c
         for y, line in enumerate(map.split('\n'), start=1)
         for x, c in enumerate(line, start=1) if c != ' '}
  path = [int(segment) if segment.isdigit() else segment
          for segment in re.split(r'([LR])', path) if segment]
  return map, path


def draw_grid(map, y, x, dy, dx):
  max_y = max(y for y, _ in map)
  max_x = max(x for _, x in map)
  arrow = '>v<^'[-dx + 1 + (dy < 0) * 2]
  for y2 in range(1, max_y + 1):
    print(''.join(arrow if y2 == y and x2 == x else map.get((y2, x2), ' ')
                  for x2 in range(1, max_x + 1)))
  print()


def part1(input):
  map, path = input
  dx = 1
  dy = 0
  y = 1
  x = min(x for y2, x in map if y2 == y)
  for segment in path:
    if isinstance(segment, int):
      for _ in range(segment):
        y2, x2 = y + dy, x + dx
        if (y2, x2) not in map:
          if dx > 0:
            x2 = min(x for y2, x in map if y2 == y)
          elif dx < 0:
            x2 = max(x for y2, x in map if y2 == y)
          elif dy > 0:
            y2 = min(y for y, x2 in map if x2 == x)
          else:
            y2 = max(y for y, x2 in map if x2 == x)
        if map[(y2, x2)] == '#':
          break
        y, x = y2, x2
    else:
      if segment == 'L':
        dy, dx = -dx, dy
      else:
        dy, dx = dx, -dy
    ## draw_grid(map, y, x, dy, dx)
    ## if msvcrt.getch() == b'\x1b':
      ## sys.exit(0)
  return 1000 * y + 4 * x + (-dx + 1 + (dy < 0) * 2)


def part2(input):
  map, path = input
  dx = 1
  dy = 0
  y = 1
  x = min(x for y2, x in map if y2 == y)
  for segment in path:
    if isinstance(segment, int):
      for _ in range(segment):
        y2, x2 = y + dy, x + dx
        dy2, dx2 = dy, dx
        if (y2, x2) not in map:
          if dx > 0:
            if y2 <= 50:
              y2, x2 = 151 - y2, 100
              dy2, dx2 = 0, -1
            elif y2 <= 100:
              y2, x2 = 50, 100 + (y2 - 50)
              dy2, dx2 = -1, 0
            elif y2 <= 150:
              y2, x2 = 51 - (y2 - 100), 150
              dy2, dx2 = 0, -1
            else:
              y2, x2 = 150, 50 + (y2 - 150)
              dy2, dx2 = -1, 0
          elif dx < 0:
            if y2 <= 50:
              y2, x2 = 151 - y2, 1
              dy2, dx2 = 0, 1
            elif y2 <= 100:
              y2, x2 = 101, (y2 - 50)
              dy2, dx2 = 1, 0
            elif y2 <= 150:
              y2, x2 = 51 - (y2 - 100), 51
              dy2, dx2 = 0, 1
            else:
              y2, x2 = 1, 50 + (y2 - 150)
              dy2, dx2 = 1, 0
          elif dy > 0:
            if x2 <= 50:
              y2, x2 = 1, 100 + x2
              dy2, dx2 = 1, 0
            elif x2 <= 100:
              y2, x2 = 150 + (x2 - 50), 50
              dy2, dx2 = 0, -1
            else:
              y2, x2 = 50 + (x2 - 100), 100
              dy2, dx2 = 0, -1
          else:
            if x2 <= 50:
              y2, x2 = 50 + x2, 51
              dy2, dx2 = 0, 1
            elif x2 <= 100:
              y2, x2 = 150 + (x2 - 50), 1
              dy2, dx2 = 0, 1
            else:
              y2, x2 = 200, (x2 - 100)
              dy2, dx2 = -1, 0
        if map[(y2, x2)] == '#':
          break
        y, x = y2, x2
        dy, dx = dy2, dx2
    else:
      if segment == 'L':
        dy, dx = -dx, dy
      else:
        dy, dx = dx, -dy
    ## draw_grid(map, y, x, dy, dx)
    ## if msvcrt.getch() == b'\x1b':
      ## sys.exit(0)
  return 1000 * y + 4 * x + (-dx + 1 + (dy < 0) * 2)


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
