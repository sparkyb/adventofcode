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

  machines = []
  for section in input.split('\n\n'):
    a_str, b_str, p_str = section.split('\n')
    a = tuple(int(n) for n in re.search(r'^Button A: X\+(\d+), Y\+(\d+)$',
                                        a_str).groups())
    b = tuple(int(n) for n in re.search(r'^Button B: X\+(\d+), Y\+(\d+)$',
                                        b_str).groups())
    prize = tuple(int(n) for n in re.search(r'^Prize: X=(\d+), Y=(\d+)$',
                                        p_str).groups())
    machines.append((a, b, prize))
  return machines


def calc_tokens(a, b, prize):
  b_tokens = round((prize[1] - prize[0] * a[1] / a[0]) /
                   (b[1] - b[0] * a[1] / a[0]))
  a_tokens = round((prize[0] - b_tokens * b[0]) / a[0])
  if all(ac * a_tokens + bc * b_tokens == pc
         for ac, bc, pc in zip(a, b, prize)):
    return 3 * a_tokens + b_tokens
  else:
    return 0


def part1(machines):
  return sum(calc_tokens(a, b, prize) for a, b, prize in machines)


def part2(machines):
  return sum(calc_tokens(a, b, tuple(p + 10000000000000 for p in prize))
             for a, b, prize in machines)


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
