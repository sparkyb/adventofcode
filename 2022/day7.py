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
import posixpath
import re
import sys

#import numpy as np


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  return input.split('\n')


def walk_dirs(input):
  cwd = '/'
  sizes = collections.defaultdict(int)
  for line in input:
    if line.startswith('$ cd '):
      cwd = posixpath.normpath(posixpath.join(cwd, line[5:]))
    elif not line.startswith('$'):
      size, name = line.split(' ', 1)
      if size != 'dir':
        size = int(size)
        path = cwd
        while True:
          sizes[path] += size
          if path == '/':
            break
          path = posixpath.dirname(path)
    else:
      assert line == '$ ls'
  return sizes


def part1(input):
  sizes = walk_dirs(input)

  return sum(size for size in sizes.values() if size <= 100000)


def part2(input):
  sizes = walk_dirs(input)

  space_remaining = 70000000 - sizes['/']
  space_needed = 30000000 - space_remaining

  return min(size for size in sizes.values() if size >= space_needed)


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
