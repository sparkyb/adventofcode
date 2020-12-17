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

  return {(x, y, 0) for y, line in enumerate(input.split('\n'))
          for x, c in enumerate(line) if c == '#'}


def neighbors(active, index):
  return sum(
      index2 in active
      for index2 in itertools.product(*(range(i - 1, i + 2) for i in index))
      if index2 != index)


def step(input):
  output = set()
  return {
      index
      for index in itertools.product(
          *(range(min(c) - 1, max(c) + 2) for c in zip(*input)))
      if (2 <= neighbors(input, index) <= 3 if index in input
          else neighbors(input, index) == 3)
  }


def part1(input):
  active = input
  for i in range(6):
    active = step(active)
  return len(active)


def part2(input):
  active = {index + (0,) for index in input}
  for i in range(6):
    active = step(active)
  return len(active)


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
