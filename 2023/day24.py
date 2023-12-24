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
import z3


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  hail = []
  for line in input.split('\n'):
    match = re.search(
        r'^(-?\d+),\s*(-?\d+),\s*(-?\d+)\s*@\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)$',
        line)
    px, py, pz, vx, vy, vz = map(int, match.groups())
    hail.append(((px, py, pz), (vx, vy, vz)))
  return hail


def intersect(p1, v1, p2, v2):
  m1 = v1[1] / v1[0]
  b1 = -m1 * p1[0] + p1[1]
  m2 = v2[1] / v2[0]
  b2 = -m2 * p2[0] + p2[1]
  try:
    x = (b2 - b1) / (m1 - m2)
  except ZeroDivisionError:
    return None
  y = m1 * x + b1
  t1 = (x - p1[0]) / v1[0]
  t2 = (x - p2[0]) / v2[0]
  if t1 < 0 or t2 < 0:
    return None
  return (x, y)


def part1(input):
  area = (200000000000000, 400000000000000)
  intersections = 0
  for (p1, v1), (p2, v2) in itertools.combinations(input, 2):
    p0 = intersect(p1, v1, p2, v2)
    if p0 and all(area[0] <= p <= area[1] for p in p0):
      intersections += 1
  return intersections


def part2(input):
  #input = input[:3]
  t = z3.IntVector('t', len(input))
  p = z3.IntVector('p0', 3)
  v = z3.IntVector('v0', 3)
  s = z3.Solver()
  for ti, (pi, vi) in zip(t, input):
    s.add(ti >= 0)
    for p1, v1, p2, v2 in zip(p, v, pi, vi):
      s.add(p1 + v1 * ti == p2 + v2 * ti)
  if s.check() == z3.sat:
    m = s.model()
    return sum(m[pi].as_long() for pi in p)


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
