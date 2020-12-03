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

  return np.array([list(line) for line in input.split('\n')]) == '#'


def count_trees(board, slope):
  y = np.arange(0, len(board), slope[0])
  x = np.arange(0, len(y) * slope[1], slope[1]) % board.shape[1]
  return np.count_nonzero(board[y, x])


def part1(input):
  return count_trees(input, (1, 3))


def part2(input):
  return functools.reduce(
      operator.mul,
      (count_trees(input, slope)
       for slope in [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]))


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
