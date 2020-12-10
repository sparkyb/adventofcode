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
  adapters = list(input)
  adapters.sort()
  adapters.insert(0, 0)
  adapters.append(adapters[-1] + 3)
  diff = defaultdict(int)
  for i in range(len(adapters) - 1):
    diff[adapters[i + 1] - adapters[i]] += 1
  return diff[1] * diff[3]


def part2(input):
  adapters = list(input)
  adapters.sort()
  adapters.insert(0, 0)

  @functools.lru_cache(maxsize=None)
  def arrangements(index):
    if index == len(adapters) - 1:
      return 1
    count = 0
    for i in range(index + 1, index + 4):
      if i >= len(adapters) or adapters[i] > adapters[index] + 3:
        break
      count += arrangements(i)
    return count

  return arrangements(0)


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
