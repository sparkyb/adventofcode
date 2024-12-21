#!/usr/bin/env python

import collections
from collections import defaultdict
import enum
import functools
import heapq
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

  return input.split('\n')


NUMERIC_KEYS = {
  '7': (0, 0),
  '8': (1, 0),
  '9': (2, 0),
  '4': (0, 1),
  '5': (1, 1),
  '6': (2, 1),
  '1': (0, 2),
  '2': (1, 2),
  '3': (2, 2),
  '0': (1, 3),
  'A': (2, 3),
}


DIR_KEYS = {
  '^': (1, 0),
  'A': (2, 0),
  '<': (0, 1),
  'v': (1, 1),
  '>': (2, 1),
}


@functools.cache
def num_moves(start, end):
  options = set()
  dx = end[0] - start[0]
  dy = end[1] - start[1]
  if dx < 0 and (start[1] < 3 or end[0] > 0):
    m = '<' * abs(dx)
    if dy < 0:
      m += '^' * abs(dy)
    elif dy > 0:
      m += 'v' * dy
    m += 'A'
    options.add(m)
  elif dx > 0:
    m = '>' * dx
    if dy < 0:
      m += '^' * abs(dy)
    elif dy > 0:
      m += 'v' * dy
    m += 'A'
    options.add(m)
  if dy < 0:
    m = '^' * abs(dy)
    if dx < 0:
      m += '<' * abs(dx)
    elif dx > 0:
      m += '>' * dx
    m += 'A'
    options.add(m)
  elif dy > 0 and (start[0] > 0 or end[1] < 3):
    m = 'v' * dy
    if dx < 0:
      m += '<' * abs(dx)
    elif dx > 0:
      m += '>' * dx
    m += 'A'
    options.add(m)
  if dx == 0 and dy == 0:
    options.add('A')
  return options


def num_dirs_length(code, n):
  if n == 0:
    return len(code)
  length = 0
  pos = NUMERIC_KEYS['A']
  for c in code:
    next_pos = NUMERIC_KEYS[c]
    options = num_moves(pos, next_pos)
    length += min(dir_dirs_length(option, n) for option in options)
    pos = next_pos
  return length


@functools.cache
def dir_moves(start, end):
  options = set()
  dx = end[0] - start[0]
  dy = end[1] - start[1]
  if dx < 0 and (start[1] > 0 or end[0] > 0):
    m = '<' * abs(dx)
    if dy < 0:
      m += '^' * abs(dy)
    elif dy > 0:
      m += 'v' * dy
    m += 'A'
    options.add(m)
  elif dx > 0:
    m = '>' * dx
    if dy < 0:
      m += '^' * abs(dy)
    elif dy > 0:
      m += 'v' * dy
    m += 'A'
    options.add(m)
  if dy < 0 and start[0] > 0:
    m = '^' * abs(dy)
    if dx < 0:
      m += '<' * abs(dx)
    elif dx > 0:
      m += '>' * dx
    m += 'A'
    options.add(m)
  elif dy > 0:
    m = 'v' * dy
    if dx < 0:
      m += '<' * abs(dx)
    elif dx > 0:
      m += '>' * dx
    m += 'A'
    options.add(m)
  if dx == 0 and dy == 0:
    options.add('A')
  return options


@functools.cache
def dir_dirs_length(code, n):
  if n == 0:
    return len(code)
  length = 0
  pos = DIR_KEYS['A']
  for c in code:
    next_pos = DIR_KEYS[c]
    options = dir_moves(pos, next_pos)
    length += min(dir_dirs_length(option, n - 1) for option in options)
    pos = next_pos
  return length


def part1(codes):
  return sum(num_dirs_length(code, 2) * int(code[:-1]) for code in codes)


def part2(codes):
  return sum(num_dirs_length(code, 25) * int(code[:-1]) for code in codes)



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
