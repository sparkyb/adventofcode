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
  files = []
  blanks = []
  i = iter(input)
  block = 0
  while True:
    try:
      size = int(next(i))
      assert size != 0
      files.append((block, size))
      block += size
      size = int(next(i))
      blanks.append((block, size))
      block += size
    except StopIteration:
      break
  return files, blanks


def part1(input):
  files, blanks = input
  files = list(files)
  blanks = list(blanks)
  checksum = 0
  for block, size in blanks:
    while size:
      block2, size2 = files[-1]
      if block2 + size2 - 1 <= block:
        break
      checksum += block * (len(files) - 1)
      block += 1
      size -= 1
      size2 -= 1
      if size2:
        files[-1] = (block2, size2)
      else:
        files.pop()
  for file_id, (block, size) in enumerate(files):
    for b in range(block, block + size):
      checksum += file_id * b
  return checksum


def part2(input):
  files, blanks = input
  files = list(files)
  blanks = list(blanks)
  for file_id in range(len(files) - 1, -1, -1):
    block, size = files[file_id]
    for i, (block2, size2) in enumerate(blanks):
      if block2 >= block:
        break
      if size2 >= size:
        files[file_id] = (block2, size)
        blanks[i] = (block2 + size, size2 - size)
        break
  return sum(file_id * b for file_id, (block, size) in enumerate(files)
             for b in range(block, block + size))


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
