import bisect
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
  input.sort()
  for a_index in range(len(input) - 1):
    a = input[a_index]
    b = 2020 - a
    b_index = bisect.bisect_left(input, b, a_index)
    if b_index != len(input) and input[b_index] == b:
      return a * b


def part2(input):
  input.sort()
  for a_index in range(len(input) - 2):
    a = input[a_index]
    for b_index in range(a_index + 1, len(input) - 1):
      b = input[b_index]
      if a + b >= 2020:
        break
      c = 2020 - a - b
      c_index = bisect.bisect_left(input, c, b_index + 1)
      if c_index != len(input) and input[c_index] == c:
        return a * b * c


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
