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

  return [(int(a), int(b), letter, password)
          for line in input.split('\n')
          for a, b, letter, password in
          [re.search(r'^(\d+)-(\d+) (\w): (\w+)$', line).groups()]]


def part1(input):
  count = 0
  for a, b, letter, password in input:
    if a <= password.count(letter) <= b:
      count += 1
  return count


def part2(input):
  count = 0
  for a, b, letter, password in input:
    if (password[a - 1] == letter) ^ (password[b - 1] == letter):
      count += 1
  return count


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
