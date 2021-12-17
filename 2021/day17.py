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

  match = re.search(r'^target area: x=(\d+)\.\.(\d+), y=(-\d+)\.\.(-\d+)$',
                    input)
  return ((int(match.group(1)), int(match.group(2))),
          (int(match.group(3)), int(match.group(4))))


def calc_x(v0, t):
  t = min(t, v0)
  return v0 * t - t * (t - 1) // 2


def calc_y(v0, t):
  return v0 * t - t * (t - 1) // 2


def find_t(y_v0, target_y):
  if y_v0 > 0:
    t = 2 * y_v0 + 2
  else:
    t = 1
  while calc_y(y_v0, t) > target_y[1]:
    t += 1
  while calc_y(y_v0, t) >= target_y[0]:
    yield t
    t += 1


def find_x_v0(target_x, t):
  x_v0 = math.ceil(target_x[0] / t)
  while calc_x(x_v0, t) < target_x[0]:
    x_v0 += 1
  while calc_x(x_v0, t) <= target_x[1]:
    yield x_v0
    x_v0 += 1


def hits_x(target_x, t):
  for x_v0 in find_x_v0(target_x, t):
    return x_v0
  return None


def find_max_y_v0(target_x, target_y):
  min_y_v0 = target_y[0]
  max_y_v0 = -target_y[0] - 1
  for y_v0 in range(max_y_v0, min_y_v0 - 1, -1):
    for t in find_t(y_v0, target_y):
      if hits_x(target_x, t):
        return y_v0
  raise AssertionError('Unreachable')


def part1(input):
  target_x, target_y = input
  y_v0 = find_max_y_v0(target_x, target_y)
  return calc_y(y_v0, y_v0)


def part2(input):
  target_x, target_y = input

  min_y_v0 = target_y[0]
  max_y_v0 = find_max_y_v0(target_x, target_y)

  v0 = set()
  for y_v0 in range(min_y_v0, max_y_v0 + 1):
    for t in find_t(y_v0, target_y):
      for x_v0 in find_x_v0(target_x, t):
        v0.add((x_v0, y_v0))

  return len(v0)


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
