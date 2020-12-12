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

  return [(line[0], int(line[1:])) for line in input.split('\n')]


DIRS = {
    'N': np.array([-1, 0]),
    'E': np.array([0, 1]),
    'S': np.array([1, 0]),
    'W': np.array([0, -1]),
}


def rotate(vector, angle):
  angle //= 90
  angle %= 4
  if angle % 2:
    vector = vector[::-1]
    vector[1] *= -1
  if angle // 2:
    vector = -vector
  return vector


def part1(input):
  dir = DIRS['E']
  ship = np.array([0, 0])
  for op, amount in input:
    if op in 'LR':
      dir = rotate(dir, amount * ((op == 'R') * 2 - 1))
    elif op == 'F':
      ship += dir * amount
    else:
      ship += DIRS[op] * amount
  return np.sum(np.abs(ship))


def part2(input):
  ship = np.array([0, 0])
  waypoint = np.array([-1, 10])  # relative to ship
  for op, amount in input:
    if op in 'LR':
      waypoint = rotate(waypoint, amount * ((op == 'R') * 2 - 1))
    elif op == 'F':
      ship += waypoint * amount
    else:
      waypoint += DIRS[op] * amount
  return np.sum(np.abs(ship))


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
