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

  return [int(''.join('1' if c in 'BR' else '0' for c in line), 2)
          for line in input.split('\n')]


def part1(input):
  return max(input)


def part2(input):
  seats = set(input)
  for i in range(0, pow(2, 11)):
    if i not in seats and i - 1 in seats and i + 1 in seats:
      return i
  return None


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
