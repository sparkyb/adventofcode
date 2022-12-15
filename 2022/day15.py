#!/usr/bin/env python

import bisect
import collections
import collections.abc
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

  return [list(map(int, re.search(r'^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$', line).groups())) for line in input.split('\n')]


class RangeSet:
  def __init__(self, iterable=()):
    self._min_x = []
    self._max_x = []
    self.update(iterable)

  def __iter__(self):
    for min_x, max_x in zip(self._min_x, self._max_x):
      yield from range(min_x, max_x + 1)

  def __len__(self):
    return sum(max_x - min_x + 1
               for min_x, max_x in zip(self._min_x, self._max_x))

  def add(self, min_x, max_x=None):
    if max_x is None:
      max_x = min_x
    if max_x < min_x:
      return
    i = bisect.bisect_right(self._min_x, min_x) - 1
    j = bisect.bisect_left(self._max_x, max_x, lo=max(i, 0))
    overlaps_start = i >= 0 and self._max_x[i] >= min_x - 1
    overlaps_end = j < len(self._min_x) and self._min_x[j] <= max_x + 1
    self._min_x[i + 1:j + overlaps_end] = [] if overlaps_start else [min_x]
    self._max_x[i + 1 - overlaps_start:j] = [] if overlaps_end else [max_x]

  def discard(self, min_x, max_x=None):
    if max_x is None:
      max_x = min_x
    if max_x < min_x:
      return
    i = bisect.bisect_right(self._min_x, min_x) - 1
    j = bisect.bisect_left(self._max_x, max_x, lo=max(i, 0))
    overlaps_start = i >= 0 and self._max_x[i] >= min_x
    overlaps_end = j < len(self._min_x) and self._min_x[j] <= max_x
    self._min_x[i + 1:j + overlaps_end] = [max_x + 1] if overlaps_end else []
    self._max_x[i + 1 - overlaps_start:j] = [min_x - 1] if overlaps_start else []

  def update(self, iterable):
    if isinstance(iterable, RangeSet):
      iterable = zip(iterable._min_x, iterable._max_x)
    for item in iterable:
      if not isinstance(item, (tuple, list)):
        item = (item,)
      self.add(*item)

  def difference_update(self, iterable):
    if isinstance(iterable, RangeSet):
      iterable = zip(iterable._min_x, iterable._max_x)
    for item in iterable:
      if not isinstance(item, (tuple, list)):
        item = (item,)
      self.discard(*item)

  def __ior__(self, iterable):
    self.update(iterable)

  def __isub__(self, iterable):
    self.difference_update(iterable)


def part1(input):
  y = 2000000
  covered = RangeSet()
  for sx, sy, bx, by in input:
    min_dist = abs(by - sy) + abs(bx - sx)
    dist = min_dist - abs(y - sy)
    covered.add(sx - dist, sx + dist)
  for sx, sy, bx, by in input:
    if by == y:
      covered.discard(bx)
  return len(covered)


def part2(input):
  y = 2000000
  sensors = []
  for y in range(0, 4000001):
    uncovered = RangeSet([(0, 4000000)])
    for sx, sy, bx, by in input:
      min_dist = abs(by - sy) + abs(bx - sx)
      dist = min_dist - abs(y - sy)
      uncovered.discard(sx - dist, sx + dist)
      if not uncovered:
        break
    if uncovered:
      assert len(uncovered) == 1
      x = next(iter(uncovered))
      return x * 4000000 + y


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
