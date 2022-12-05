#!/usr/bin/env python

import collections
from collections import defaultdict
import copy
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

  top, bottom = input.split('\n\n')
  stacks = collections.defaultdict(list)
  for line in list(reversed(top.split('\n')))[1:]:
    for i in range(1, 10):
      crate = line[(i - 1) * 4 + 1]
      if crate != ' ':
        stacks[i].append(crate)
  steps = [list(map(int, re.search(r'^move (\d+) from (\d+) to (\d+)$', line).groups())) for line in bottom.split('\n')]
  return stacks, steps


def part1(input):
  stacks, steps = input
  stacks = copy.deepcopy(stacks)
  for n, f, t in steps:
    for i in range(n):
      stacks[t].append(stacks[f].pop())
  return ''.join(stacks[i][-1] for i in range(1, 10))


def part2(input):
  stacks, steps = input
  stacks = copy.deepcopy(stacks)
  for n, f, t in steps:
    stacks[t].extend(stacks[f][-n:])
    stacks[f][-n:] = []
  return ''.join(stacks[i][-1] for i in range(1, 10))


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
