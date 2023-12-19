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


DIRS = {
    'R': (0, 1),
    'D': (1, 0),
    'L': (0, -1),
    'U': (-1, 0),
}


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  ret = []
  for line in input.split('\n'):
    match = re.search(r'^([RDLU]) (\d+) \(#([0-9a-f]{5})([0-3])\)$', line)
    ret.append((
        (DIRS[match.group(1)], int(match.group(2))),
        (DIRS['RDLU'[int(match.group(4))]], int(match.group(3), 16)),
    ))
  return ret


def build_border(turns):
  y, x = 0, 0
  corners = []
  for (dy, dx), dist in turns:
    corners.append((y, x))
    y = y + dy * dist
    x = x + dx * dist
  assert (y, x) == (0, 0)
  return corners


def line_area(corners, y):
  crossings = []
  for i, (y1, x1) in enumerate(corners):
    y2, x2 = corners[(i + 1) % len(corners)]
    if y1 == y:
      # corner in this line
      y0, x0 = corners[(i - 1) % len(corners)]
      corner = ((y2 - y0) / (x2 - x0) > 0) * 2 - 1
      crossings.append((x1, corner))
    elif min(y1, y2) < y < max(y1, y2):
      # crossing vertical line in the middle
      crossings.append((x1, 0))
  crossings.sort()
  if not crossings:
    return 0
  area = 1
  prev_x, prev_corner = crossings[0]
  inside = not prev_corner
  for x, corner in crossings[1:]:
    if prev_corner:
      assert corner
      area += x - prev_x
      if corner == prev_corner:
        inside = not inside
      prev_corner = 0
    else:
      if inside:
        area += x - prev_x
      else:
        area += 1
      if corner:
        prev_corner = corner
      else:
        inside = not inside
    prev_x = x
  return area


def calc_area(turns):
  corners = build_border(turns)
  lines = sorted({y for y, _ in corners})
  area = sum(line_area(corners, y) for y in lines)
  for y1, y2 in zip(lines, lines[1:]):
    area += line_area(corners, y1 + 1) * (y2 - y1 - 1)
  return area


def part1(input):
  return calc_area(turn for turn, _ in input)


def part2(input):
  return calc_area(turn for _, turn in input)


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
