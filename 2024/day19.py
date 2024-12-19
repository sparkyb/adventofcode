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

  towels, designs = input.split('\n\n')
  towels = tuple(sorted(towels.split(', '), key=len, reverse=True))
  designs = designs.split('\n')
  return towels, designs


@functools.cache
def pattern_possible(design, towels):
  return any(design.startswith(towel) and
             (len(design) == len(towel) or
              pattern_possible(design[len(towel):], towels))
             for towel in towels)


@functools.cache
def count_patterns(design, towels):
  return sum(1 if len(design) == len(towel)
             else count_patterns(design[len(towel):], towels)
             for towel in towels if design.startswith(towel))


def part1(input):
  towels, designs = input
  return sum(1 for design in designs if pattern_possible(design, towels))


def part2(input):
  towels, designs = input
  return sum(count_patterns(design, towels) for design in designs)


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
