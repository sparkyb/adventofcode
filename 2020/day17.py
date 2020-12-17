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

import numpy as np


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  return np.array([[[c == '#' for c in line] for line in input.split('\n')]])


def neighbors(input, index):
  active = all(0 <= i < s for i, s in zip(index, input.shape)) and input[index]
  return active, np.count_nonzero(
      input[tuple(slice(max(i - 1, 0), min(i + 2, s))
                  for i, s in zip(index, input.shape))]) - active


def step(input):
  output = np.full([d + 2 for d in input.shape], False)
  for index in np.ndindex(*output.shape):
    active, n = neighbors(input, tuple(i - 1 for i in index))
    if active:
      output[index] = 2 <= n <= 3
    else:
      output[index] = n == 3
  return output[tuple(slice(min(c), max(c) + 1) for c in np.nonzero(output))]


def part1(input):
  for i in range(6):
    input = step(input)
  return np.count_nonzero(input)


def part2(input):
  input = input[np.newaxis, ...]
  for i in range(6):
    input = step(input)
  return np.count_nonzero(input)


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
