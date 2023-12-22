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

  bricks = {}
  for line in input.split('\n'):
    match = re.search(r'^(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)$', line)
    x1, y1, z1, x2, y2, z2 = map(int, match.groups())
    dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
    if dx:
      dx //= abs(dx)
    if dy:
      dy //= abs(dy)
    if dz:
      dz //= abs(dz)
    x, y, z = x1, y1, z1
    brick = [(x, y, z)]
    while x != x2 or y != y2 or z != z2:
      x += dx
      y += dy
      z += dz
      brick.append((x, y, z))
    bricks[len(bricks)] = tuple(brick)
  return bricks


def brick_bottom(brick):
  return min(z for _, _, z in brick[1])


def settle(bricks):
  prev_bricks = None
  while bricks != prev_bricks:
    prev_bricks = bricks
    bricks = {}
    cubes = set()
    for key, brick in sorted(prev_bricks.items(), key=brick_bottom):
      if any(z <= 1 for _, _, z in brick):
        bricks[key] = brick
        cubes.update(brick)
        continue
      dropped = tuple((x, y, z - 1) for x, y, z in brick)
      if any(cube in cubes for cube in dropped):
        bricks[key] = brick
        cubes.update(brick)
        continue
      bricks[key] = dropped
      cubes.update(dropped)
  return bricks


def part1(input):
  bricks = settle(input)
  cubes = {}
  for key, brick in bricks.items():
    for cube in brick:
      cubes[cube] = key
  total = 0
  for remove in bricks:
    for key, brick in bricks.items():
      if key == remove:
        continue
      for x, y, z in brick:
        if z <= 1:
          break
        cube = (x, y, z - 1)
        if cubes.get(cube, None) not in (None, remove, key):
          break
      else:
        break
    else:
      total += 1
  return total


def part2(input):
  bricks = settle(input)
  total = 0
  for remove in bricks:
    new_bricks = {key: brick for key, brick in bricks.items() if key != remove}
    total += sum(new_bricks[key] != brick
                 for key, brick in settle(new_bricks).items())
  return total


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
