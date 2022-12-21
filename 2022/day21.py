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

  ret = {}
  for line in input.split('\n'):
    k, v, v1, o, v2 = re.search(
        r'^(\w{4}): (?:(\d+)|(\w{4}) ([-+*/]) (\w{4}))$', line).groups()
    ret[k] = int(v) if v else (v1, o, v2)
  return ret


def part1(input):
  values = {}
  while 'root' not in values:
    for k, v in input.items():
      if isinstance(v, int):
        values[k] = v
      else:
        v1, o, v2 = v
        if v1 in values and v2 in values:
          if o == '+':
            values[k] = values[v1] + values[v2]
          elif o == '-':
            values[k] = values[v1] - values[v2]
          elif o == '*':
            values[k] = values[v1] * values[v2]
          elif o == '/':
            values[k] = values[v1] // values[v2]
  return values['root']


def part2(input):
  values = {}
  while 'root' not in values:
    for k, v in input.items():
      if k == 'humn':
        values[k] = 'x'
      elif isinstance(v, int):
        values[k] = v
      else:
        v1, o, v2 = v
        if v1 in values and v2 in values:
          if k == 'root':
            o = '='
          if isinstance(values[v1], int) and isinstance(values[v2], int):
            if o == '+':
              values[k] = values[v1] + values[v2]
            elif o == '-':
              values[k] = values[v1] - values[v2]
            elif o == '*':
              values[k] = values[v1] * values[v2]
            elif o == '/':
              values[k] = values[v1] // values[v2]
          else:
            values[k] = (values[v1], o, values[v2])
  expr = values['root']
  if isinstance(expr[0], int):
    value, _, expr = expr
  else:
    expr, _, value = expr
  while expr != 'x':
    if isinstance(expr[0], int):
      v, o, expr = expr
      if o == '+':
        value -= v
      elif o == '-':
        value = v - value
      elif o == '*':
        value //= v
      elif o == '/':
        value = v // value
    else:
      expr, o, v = expr
      if o == '+':
        value -= v
      elif o == '-':
        value += v
      elif o == '*':
        value //= v
      elif o == '/':
        value *= v
  return value


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
