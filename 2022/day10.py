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
    op, *args = line.split(' ')
    args = list(map(int, args))
    ret.append((op, args))
  return ret


def run_code(input):
  x = [1]
  for op, args in input:
    if op == 'addx':
      x.append(x[-1])
      x.append(x[-1] + args[0])
    elif op == 'noop':
      x.append(x[-1])
  return x


def part1(input):
  x = run_code(input)
  return sum(cycle * x[cycle - 1] for cycle in range(20, 221, 40))


def part2(input):
  sprite_x = run_code(input)
  
  for y in range(6):
    print(''.join('#' if x - 1 <= sprite_x[y * 40 + x] <= x + 1 else '.' for x in range(40)))


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
