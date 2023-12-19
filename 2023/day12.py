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

  return [(springs, [int(c) for c in counts.split(',')])
          for springs, counts in (line.split() for line in input.split('\n'))]


@functools.lru_cache
def spring_permutations(springs, counts):
  springs = springs.strip('.')
  if not counts:
    return '#' not in springs
  if len(springs) < counts[0]:
    return 0
  if springs[0] == '#':
    if re.search(r'^[?#]{' + str(counts[0]) + r'}([?.]|$)', springs):
      return spring_permutations(springs[counts[0] + 1:], counts[1:])
    else:
      return 0
  else:
    return (spring_permutations('#' + springs[1:], counts) +
            spring_permutations(springs[1:], counts))


def part1(input):
  return sum(spring_permutations(springs, tuple(counts))
             for springs, counts in input)


def part2(input):
  return sum(spring_permutations('?'.join([springs] * 5), tuple(counts * 5))
             for springs, counts in input)


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
