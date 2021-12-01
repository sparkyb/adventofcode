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


def part1(input):
  for i in range(25, len(input)):
    for a, b in itertools.combinations(input[i - 25:i], 2):
      if a + b == input[i]:
        break
    else:
      return input[i]


def part2(input):
  target = part1(input)
  a = b = s = 0
  while s != target:
    if s < target:
      s += input[b]
      b += 1
    else:
      s -= input[a]
      a += 1
  return min(input[a:b]) + max(input[a:b])


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
