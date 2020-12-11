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

  return np.array([list(line) for line in input.split('\n')])


class Done(Exception):
  pass


def step1(prev):
  changed = False
  next = np.copy(prev)
  padded = np.pad(prev, ((1, 1), (1, 1)), constant_values='.')
  for y, x in np.argwhere(prev != '.'):
    count = np.count_nonzero(padded[y:y + 3, x:x + 3] == '#')
    if prev[y, x] == 'L' and count == 0:
      changed = True
      next[y, x] = '#'
    elif prev[y, x] == '#' and count >= 5:
      changed = True
      next[y, x] = 'L'
  if changed:
    return next
  else:
    raise Done()


def part1(input):
  while True:
    ## print('\n'.join(''.join(line) for line in input))
    ## print()
    ## msvcrt.getch()
    try:
      input = step1(input)
    except Done:
      return np.count_nonzero(input == '#')


def step2(prev):
  changed = False
  next = np.copy(prev)
  for y, x in np.argwhere(prev != '.'):
    count = 0
    for dy, dx in np.nditer(np.ogrid[-1:2, -1:2]):
      if dy == 0 and dx == 0:
        continue
      y2, x2 = y + dy, x + dx
      while 0 <= y2 < prev.shape[0] and 0 <= x2 < prev.shape[1]:
        if prev[y2, x2] != '.':
          count += prev[y2, x2] == '#'
          break
        y2 += dy
        x2 += dx
      if prev[y, x] == 'L' and count or count >= 5:
        break
    if prev[y, x] == 'L' and count == 0:
      changed = True
      next[y, x] = '#'
    elif prev[y, x] == '#' and count >= 5:
      changed = True
      next[y, x] = 'L'
  if changed:
    return next
  else:
    raise Done()


def part2(input):
  while True:
    ## print('\n'.join(''.join(line) for line in input))
    ## print()
    ## msvcrt.getch()
    try:
      input = step2(input)
    except Done:
      return np.count_nonzero(input == '#')


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
