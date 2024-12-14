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

  robots = []
  for line in input.split('\n'):
    match = re.search(r'^p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)$', line)
    px, py, vx, vy = (int(n) for n in match.groups())
    robots.append(((px, py), (vx, vy)))
  return robots


def simulate(robots, size, steps=1):
  return [(tuple((p + v * steps) % s for p, v, s in zip(pos, vel, size)), vel)
          for pos, vel in robots]


def safety_factor(robots, size):
  quadrants = collections.defaultdict(int)
  for pos, _ in robots:
    quad = tuple((p - s // 2) for p, s in zip(pos, size))
    if all(quad):
      quadrants[tuple(q > 0 for q in quad)] += 1
  return math.prod(quadrants.values())


def draw(robots, size):
  positions = {pos for pos, vel in robots}
  for y in range(size[1]):
    print(''.join('.*'[(x, y) in positions] for x in range(size[0])))
  print()


def part1(robots):
  size = (101, 103)
  return safety_factor(simulate(robots, size, 100), size)


def part2(robots):
  size = (101, 103)
  for i in range(1, math.prod(size)):
    if i % size[0] == 46 and i % size[1] == 1:
      robots2 = simulate(robots, size, i)
      draw(robots2, size)
      return i
      print(i)
      if msvcrt.getch() == b'\x1b':
        return i


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
