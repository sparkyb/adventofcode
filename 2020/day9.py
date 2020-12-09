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
    for a in range(i - 25, i):
      for b in range(a, i):
        if input[a] + input[b] == input[i]:
          break
      else:
        continue
      break
    else:
      return input[i]


def part2(input):
  target = part1(input)
  for i in range(0, len(input)):
    for l in range(2, len(input) - i + 1):
      s = sum(input[i:i + l])
      if s == target:
        return min(input[i:i + l]) + max(input[i:i + l])
      elif s > target:
        break


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
