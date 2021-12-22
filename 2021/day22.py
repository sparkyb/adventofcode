#!/usr/bin/env python

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


class Cube(tuple):
  def __bool__(self):
    return all(x >= n for n, x in self)

  def __xor__(self, other):
    if not isinstance(other, Cube):
      raise TypeError(f'unsupported operand type(s) for ^: '
                      '{type(self).__name__!r} and {type(other).__name__!r}')
    return Cube((max(s[0], o[0]), min(s[1], o[1])) for s, o in zip(self, other))

  def __sub__(self, other):
    if not isinstance(other, Cube):
      raise TypeError(f'unsupported operand type(s) for -: '
                      '{type(self).__name__!r} and {type(other).__name__!r}')
    mid = self ^ other
    if not mid:
      return [self]
    ret = []
    for i, (s, o) in enumerate(zip(self, other)):
      if o[0] > s[0]:
        ret.append(Cube(mid[:i] + ((s[0], o[0] - 1),) + self[i + 1:]))
      if o[1] < s[1]:
        ret.append(Cube(mid[:i] + ((o[1] + 1, s[1]),) + self[i + 1:]))
    return ret

  @property
  def volume(self):
    if not self:
      return 0
    return math.prod(x - n + 1 for n, x in self)


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  steps = []
  for line in input.split('\n'):
    on_off, cube_s = line.split()
    cube = Cube(
        tuple(map(int, re.search(r'^[xyz]=(-?\d+)\.\.(-?\d+)$', axis).groups()))
        for axis in cube_s.split(','))
    steps.append((on_off == 'on', cube))
  return steps


def part1(steps):
  cubes = set()
  for on, cube in steps:
    for point in itertools.product(*(range(max(n, -50), min(x, 50) + 1)
                                     for n, x in cube)):
      if on:
        cubes.add(point)
      else:
        cubes.discard(point)
  return len(cubes)


def part2(steps):
  cubes = []
  for on, new_cube in steps:
    new_cubes = []
    for cube in cubes:
      new_cubes.extend(cube - new_cube)
    if on:
      new_cubes.append(new_cube)
    cubes = new_cubes
  return sum(cube.volume for cube in cubes)


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
