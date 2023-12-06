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

  return list(zip(*(map(int, line.split()[1:]) for line in input.split('\n'))))


def quadratic_formula(a, b, c):
  return (
      (-b + math.sqrt(pow(b, 2) - 4 * a * c)) / (2 * a),
      (-b - math.sqrt(pow(b, 2) - 4 * a * c)) / (2 * a),
  )


def race_wins(duration, min_distance):
  ## return sum(t * (duration - t) > min_distance for t in range(1, duration))
  try:
    t1, t2 = quadratic_formula(1, -duration, min_distance)
  except ValueError:
    return 0
  if t1 > t2:
    t1, t2 = t2, t1
  t1 = min(max(math.floor(t1) + 1, 0), duration)
  t2 = min(max(math.ceil(t2) - 1, 0), duration)
  return t2 - t1 + 1


def part1(input):
  return math.prod(
      race_wins(duration, min_distance)
      for duration, min_distance in input)


def part2(input):
  duration, min_distance = [int(''.join(str(n) for n in values))
                            for values in zip(*input)]
  return race_wins(duration, min_distance)


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
