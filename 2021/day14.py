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

  template, rules = input.split('\n\n')
  rules = dict(line.split(' -> ') for line in rules.split('\n'))
  return template, rules


def step1(template, rules):
  ret = []
  for i, c in enumerate(template):
    if i > 0:
      ret.append(rules[template[i - 1:i + 1]])
    ret.append(c)
  return ''.join(ret)


def part1(input):
  template, rules = input
  for i in range(10):
    template = step1(template, rules)
  counts = collections.Counter(template)
  counts = sorted(counts.values())
  return counts[-1] - counts[0]


def get_pairs(template):
  return collections.Counter(template[i:i + 2]
                             for i in range(len(template) - 1))


def step2(pairs, rules):
  ret = collections.Counter()
  for pair, count in pairs.items():
    middle = rules[pair]
    ret[pair[0] + middle] += count
    ret[middle + pair[1]] += count
  return ret


def part2(input):
  template, rules = input
  pairs = get_pairs(template)
  for i in range(40):
    pairs = step2(pairs, rules)
  counts = collections.Counter(template[0] + template[-1])
  for pair, count in pairs.items():
    counts[pair[0]] += count
    counts[pair[1]] += count
  for pair in counts:
    counts[pair] //= 2
  counts = sorted(counts.values())
  return counts[-1] - counts[0]


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
