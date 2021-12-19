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


class Vector(tuple):
  def rotate(self, axis, n=1):
    n %= 4
    if n == 0:
      return self
    axes = ((axis + 1) % 3, (axis + 2) % 3)
    rotated = list(self)
    for _ in range(n):
      rotated[axes[0]], rotated[axes[1]] = rotated[axes[1]], -rotated[axes[0]]
    return type(self)(rotated)

  def __add__(self, other):
    if not isinstance(other, Vector):
      raise TypeError(f'unsupported operand type(s) for +: '
                      '{type(self).__name__!r} and {type(other).__name__!r}')
    return type(self)(a + b for a, b in zip(self, other))

  def __sub__(self, other):
    if not isinstance(other, Vector):
      raise TypeError(f'unsupported operand type(s) for -: '
                      '{type(self).__name__!r} and {type(other).__name__!r}')
    return type(self)(a - b for a, b in zip(self, other))

  def __neg__(self):
    return type(self)(-n for n in self)

  @property
  def manhattan_length(self):
    return sum(abs(n) for n in self)

  def __str__(self):
    return ','.join(map(str, self))


class Scanner(tuple):
  def __init__(self, beacons, position=Vector((0, 0, 0))):
    self.position = position

  def rotate(self, axis, n=1):
    n %= 4
    if n == 0:
      return self
    return type(self)((beacon.rotate(axis, n) for beacon in self),
                      position=self.position.rotate(axis, n))

  def __add__(self, offset):
    if not isinstance(offset, Vector):
      raise TypeError(f'unsupported operand type(s) for +: '
                      '{type(self).__name__!r} and {type(offset).__name__!r}')
    return type(self)((beacon + offset for beacon in self),
                      position=self.position + offset)

  def rotations(self):
    for i in range(4):
      beacons2 = self.rotate(2, i)
      for j in range(4):
        yield beacons2.rotate(0, j)
    for i in (-1, 1):
      beacons2 = self.rotate(1, i)
      for j in range(4):
        yield beacons2.rotate(0, j)

  @property
  def distances(self):
    if not hasattr(self, '_distances'):
      self._distances = collections.defaultdict(set)
      for i, beacon1 in enumerate(self):
        for j, beacon2 in enumerate(self[i + 1:], start=i + 1):
          self._distances[(beacon1 - beacon2).manhattan_length].update((i, j))
    return self._distances

  def match(self, other):
    matched_distances = set(self.distances) & set(other.distances)
    if len(matched_distances) < math.comb(12, 2):
      return None
    for distance in matched_distances:
      for rotated in other.rotations():
        for i in self.distances[distance]:
          beacon0 = self[i]
          for j in other.distances[distance]:
            beacon1 = rotated[j]
            offset = beacon0 - beacon1
            translated = rotated + offset
            if len(set(translated) & set(self)) >= 12:
              return translated
    return None

  def __str__(self):
    return '\n'.join(map(str, self))


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  return {
      i: Scanner(
          Vector(map(int, re.search(r'^(-?\d{1,3}),(-?\d{1,3}),(-?\d{1,3})$',
                                    beacon).groups()))
          for beacon in scanner.split('\n')[1:]
      )
      for i, scanner in enumerate(input.split('\n\n'))
  }


def match_scanners(scanners):
  matched = {0: scanners[0]}
  unmatched = dict(scanners)
  unmatched.pop(0)
  skip = set()
  while unmatched:
    for i, j in itertools.product(matched, unmatched):
      if (i, j) in skip:
        continue
      beacons0 = matched[i]
      beacons1 = unmatched[j]
      aligned = beacons0.match(beacons1)
      if aligned:
        matched[j] = aligned
        unmatched.pop(j)
        break
      else:
        skip.add((i, j))
  return matched


def part1(scanners):
  matched = match_scanners(scanners)
  return len(functools.reduce(set.union, matched.values(), set()))


def part2(scanners):
  matched = match_scanners(scanners)
  return max(
      (scanner1.position - scanner2.position).manhattan_length
      for scanner1, scanner2 in itertools.combinations(matched.values(), 2))


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
