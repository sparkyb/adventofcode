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

  return {(y, x): c == '#' for y, line in enumerate(input.split('\n'))
          for x, c in enumerate(line) if c != '.'}


DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


class Done(Exception):
  pass


def step1(prev):
  changed = False
  next = {}
  for y, x in prev:
    count = sum(prev.get((y + dy, x + dx), False) for dy, dx in DIRS)
    if (count >= 4) if prev[(y, x)] else (count == 0):
      changed = True
      next[(y, x)] = not prev[(y, x)]
    else:
      next[(y, x)] = prev[(y, x)]
  if changed:
    return next
  else:
    raise Done()


def part1(input):
  while True:
    try:
      input = step1(input)
    except Done:
      return sum(input.values())


def step2(prev):
  changed = False
  next = {}
  max_y, max_x = functools.reduce(
      lambda k, max_k: tuple(map(max, zip(k, max_k))),
      prev.keys(),
      (0, 0))
  for y, x in prev:
    count = 0
    for dy, dx in DIRS:
      y2, x2 = y + dy, x + dx
      while 0 <= y2 <= max_y and 0 <= x2 <= max_x:
        if (y2, x2) in prev:
          count += prev[(y2, x2)]
          break
        y2 += dy
        x2 += dx
      if (count >= 5) if prev[(y, x)] else count:
        break
    if (count >= 5) if prev[(y, x)] else (count == 0):
      changed = True
      next[(y, x)] = not prev[(y, x)]
    else:
      next[(y, x)] = prev[(y, x)]
  if changed:
    return next
  else:
    raise Done()


def part2(input):
  while True:
    try:
      input = step2(input)
    except Done:
      return sum(input.values())


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
