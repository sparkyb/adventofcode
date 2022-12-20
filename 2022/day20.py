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

  return list(map(int, input.split('\n')))


def mix(numbers, rounds=1):
  indexes = collections.deque(range(len(numbers)))
  for round in range(rounds):
    for i in range(len(numbers)):
      indexes.rotate(-indexes.index(i))
      indexes.popleft()
      indexes.rotate(-numbers[i])
      indexes.append(i)
  return [numbers[i] for i in indexes]


def part1(input):
  numbers = mix(input)
  zero = numbers.index(0)
  return sum(numbers[(zero + i) % len(numbers)] for i in (1000, 2000, 3000))


def part2(input):
  numbers = mix([n * 811589153 for n in input], 10)
  zero = numbers.index(0)
  return sum(numbers[(zero + i) % len(numbers)] for i in (1000, 2000, 3000))


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
