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


CONSTANTS_RE = re.compile(r"""
inp w
mul x 0
add x z
mod x 26
div z (1|26)
add x (-?\d+)
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y (\d+)
mul y x
add z y
""".strip())


def find_constants(input):
  constants = [tuple(map(int, matches))
               for matches in CONSTANTS_RE.findall(input)]
  assert len(constants) == 14
  return constants


def find_equasions(constants):
  equasions = []
  z = []
  for i, (div, a, b) in enumerate(constants):
    if div == 26:
      j, b = z.pop()
      equasions.append((i, j, a + b))
    else:
      z.append((i, b))
  assert not z
  return equasions


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  return find_equasions(find_constants(input))


def part1(equasions):
  digits = [0] * 14
  for i, j, c in equasions:
    if c >= 0:
      digits[i] = 9
      digits[j] = 9 - c
    else:
      digits[j] = 9
      digits[i] = 9 + c
  return functools.reduce((lambda n, d: n * 10 + d), digits, 0)


def part2(equasions):
  digits = [0] * 14
  for i, j, c in equasions:
    if c >= 0:
      digits[j] = 1
      digits[i] = 1 + c
    else:
      digits[i] = 1
      digits[j] = 1 - c
  return functools.reduce((lambda n, d: n * 10 + d), digits, 0)


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
