#!/usr/bin/env python

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

  ret = []
  for line in input.split('\n'):
    line = line.split(' ')
    ret.append((line[0], int(line[1])))
  return ret


DIRS = {
  'U': (-1, 0),
  'D': (1, 0),
  'L': (0, -1),
  'R': (0, 1),
}


def sign(x):
  return (x > 0) - (x < 0)


def move(knots, dir):
  dy, dx = DIRS[dir]
  knots[0] = (knots[0][0] + dy, knots[0][1] + dx)
  for i in range(len(knots) - 1):
    dy = knots[i][0] - knots[i + 1][0]
    dx = knots[i][1] - knots[i + 1][1]
    d = max(abs(dy), abs(dx)) - 1
    dy = d * sign(dy)
    dx = d * sign(dx)
    knots[i + 1] = (knots[i + 1][0] + dy, knots[i + 1][1] + dx)


def part1(input):
  knots = [(0, 0), (0, 0)]
  visited = set([knots[-1]])
  for dir, n in input:
    while n:
      move(knots, dir)
      visited.add(knots[-1])
      n -= 1
  return len(visited)


def part2(input):
  knots = [(0, 0) for i in range(10)]
  visited = set([knots[-1]])
  for dir, n in input:
    while n:
      move(knots, dir)
      visited.add(knots[-1])
      n -= 1
  return len(visited)


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('-c', '--clip', '--copy', action='store_true',
                      help='Copy answer to clipboard')
  parser.add_argument('-p', '--part', type=int, choices=(1, 2),
                      help='Which part to run (default: both)')
  parser.add_argument('-1', '--part1', action='store_const', dest='part',
                      const=1, help='Part 1 only')
  parser.add_argument('-2', '--part2', action='store_const', dest='part',
                      const=2, help='Part 2 only')
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  if args.clip:
    import pyperclip
  input = get_input(args.input)
  if not args.part or args.part == 1:
    answer1 = part1(input)
    print(answer1)
    if args.clip and answer1 is not None:
      pyperclip.copy(str(answer1))
  if not args.part or args.part == 2:
    answer2 = part2(input)
    print(answer2)
    if args.clip and answer2 is not None:
      pyperclip.copy(str(answer2))
