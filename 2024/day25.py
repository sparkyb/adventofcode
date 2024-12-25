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

  sections = input.split('\n\n')

  locks = []
  keys = []
  for section in sections:
    rows = section.split('\n')
    columns = [''.join(segments) for segments in zip(*rows)]
    if all(c == '#' for c in rows[0]):
      # lock
      locks.append(tuple(max(y for y, c in enumerate(column) if c == '#')
                         for column in columns))
    else:
      # key
      keys.append(tuple(max(y for y, c in enumerate(reversed(column))
                            if c == '#')
                        for column in columns))
  return locks, keys


def part1(input):
  locks, keys = input
  return sum(all(l + k <= 5 for l, k in zip(lock, key))
             for lock, key in itertools.product(locks, keys))


def part2(input):
  return None


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
