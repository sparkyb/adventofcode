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

  return input.split(',')


def hash(s):
  value = 0
  for c in s:
    value += ord(c)
    value *= 17
    value %= 256
  return value


def part1(input):
  return sum(hash(s) for s in input)


def part2(input):
  boxes = collections.defaultdict(collections.OrderedDict)
  for step in input:
    match = re.search(r'^(\w+)(=[1-9]|-)$', step)
    label = match.group(1)
    box = hash(label)
    op = match.group(2)
    if op[0] == '-':
      boxes[box].pop(label, None)
    else:
      focal_length = int(op[1:])
      boxes[box][label] = focal_length
  return sum((box + 1) * (slot + 1) * focal_length
             for box, lenses in boxes.items()
             for slot, focal_length in enumerate(lenses.values()))
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
