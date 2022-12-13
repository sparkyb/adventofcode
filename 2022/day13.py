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

  pairs = []
  for lines in input.split('\n\n'):
    pairs.append([eval(line) for line in lines.split('\n')])
  return pairs


def compare(left, right):
  if isinstance(left, int) and isinstance(right, int):
    return left - right
  elif isinstance(left, int):
    left = [left]
  elif isinstance(right, int):
    right = [right]
  for l, r in itertools.zip_longest(left, right):
    if l is None:
      return -1
    elif r is None:
      return 1
    result = compare(l, r)
    if result:
      return result
  return 0


def part1(input):
  return sum(i for i, pair in enumerate(input, start=1) if compare(*pair) < 0)


def part2(input):
  dividers = [[[2]], [[6]]]
  packets = sorted(itertools.chain(dividers, *input),
                   key=functools.cmp_to_key(compare))
  return math.prod(packets.index(divider) + 1 for divider in dividers)


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
