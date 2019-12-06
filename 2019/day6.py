from collections import defaultdict
import itertools
import math
from hashlib import md5
import msvcrt
#import numpy as np
import os.path
import re
import sys

from intcode import Intcode


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip()

  return dict(reversed(line.split(')')) for line in input.split('\n'))


def ancestors(orbits, obj, memo={}):
  if obj in memo:
    return memo[obj]
  around = orbits.get(obj)
  if around:
    ret = [around] + ancestors(orbits, around, memo)
  else:
    ret = []
  memo[obj] = ret
  return ret


def part1(input):
  orbits = 0
  for obj in input:
    orbits += len(ancestors(input, obj))
  return orbits


def part2(input):
  transfers = 0
  you_ancestors = ancestors(input, 'YOU')
  san_ancestors = ancestors(input, 'SAN')
  return len(set(you_ancestors) ^ set(san_ancestors))


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
