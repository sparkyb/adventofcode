import collections
from collections import defaultdict
import enum
import functools
import itertools
import math
import msvcrt
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


def part1(input):
  for i, a in enumerate(input):
    for b in input[i + 1:]:
      if a + b == 2020:
        return a * b


def part2(input):
  for i, a in enumerate(input):
    for j, b in enumerate(input[i + 1:], start=i + 1):
      for c in input[j + 1:]:
        if a + b + c == 2020:
          return a * b * c


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
