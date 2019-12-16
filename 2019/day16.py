from collections import defaultdict
import enum
import functools
import itertools
import math
from hashlib import md5
import msvcrt
import numpy as np
import os.path
import re
import sys

from intcode import Intcode


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip()

  return list(map(int, input))


def pattern(digit):
  base = [0, 1, 0, -1]
  first = True
  while True:
    for i, d in enumerate(base):
      for j in range(digit + 1):
        if first:
          first = False
          continue
        yield d


def part1(input):
  input = np.array(input)
  patterns = np.array([list(itertools.islice(pattern(i), len(input))) for i in range(len(input))])

  for phase in range(100):
    input = np.mod(np.abs(patterns @ input), 10)
  return ''.join(str(d) for d in input[:8])


def part2(input):
  offset = int(''.join(str(d) for d in input[:7]))
  input = np.array(input * 10000)

  input = input[:offset - 1:-1]
  for phase in range(100):
    input = np.mod(np.cumsum(input), 10)
  return ''.join(str(d) for d in input[:-9:-1])


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
