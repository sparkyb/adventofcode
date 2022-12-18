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

  return {tuple(map(int, line.split(','))) for line in input.split('\n')}


def part1(input):
  area = 0
  for cube in input:
    for axis in range(3):
      for delta in (-1, 1):
        cube2 = tuple(v + (delta if i == axis else 0)
                      for i, v in enumerate(cube))
        area += cube2 not in input
  return area


def is_outside(cubes, bounds, cube, outside, inside):
  if cube in cubes or cube in inside:
    return False
  if cube in outside:
    return True
  visited = set()
  frontier = [cube]
  while frontier:
    cube = frontier.pop()
    if cube in cubes or cube in visited:
      continue
    visited.add(cube)
    if (cube in outside or
        any(cube[axis] <= bounds[0][axis] or cube[axis] >= bounds[1][axis]
            for axis in range(3))):
      outside.update(visited)
      return True
    elif cube in inside:
      break
    else:
      for axis in range(3):
        for delta in (-1, 1):
          cube2 = tuple(v + (delta if i == axis else 0)
                        for i, v in enumerate(cube))
          frontier.append(cube2)
  inside.update(visited)
  return False


def part2(input):
  bounds = [tuple(min(cube[axis] for cube in input) for axis in range(3)),
            tuple(max(cube[axis] for cube in input) for axis in range(3))]
  outside = set()
  inside = set()
  area = 0
  for cube in input:
    for axis in range(3):
      for delta in (-1, 1):
        cube2 = tuple(v + (delta if i == axis else 0)
                      for i, v in enumerate(cube))
        area += is_outside(input, bounds, cube2, outside, inside)
  return area


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
