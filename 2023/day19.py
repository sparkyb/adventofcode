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

  workflow_lines, part_lines = input.split('\n\n')

  workflows = {}
  for line in workflow_lines.split('\n'):
    match = re.search(
        r'^([a-z]+){((?:[xmas][><]\d+:(?:[a-z]+|[AR]),)*)([a-z]+|[AR])}$',
        line)
    name = match.group(1)
    rules = []
    for var, op, value, dest in re.findall(
        r'([xmas])([><])(\d+):([a-z]+|[AR]),',
        match.group(2)):
      value = int(value)
      if dest in 'AR':
        dest = bool('RA'.index(dest))
      rules.append((var, op, value, dest))
    default = match.group(3)
    if default in 'AR':
      default = bool('RA'.index(default))
    workflows[name] = (rules, default)

  parts = []
  parts = [
      {k: int(v) for k, v in re.search(
          r'^{x=(?P<x>\d+),m=(?P<m>\d+),a=(?P<a>\d+),s=(?P<s>\d+)}$',
          line).groupdict().items()}
      for line in part_lines.split('\n')
  ]

  return workflows, parts


def part1(input):
  workflows, parts = input
  total = 0
  for part in parts:
    workflow = 'in'
    while isinstance(workflow, str):
      for var, op, value, dest in workflows[workflow][0]:
        if ((op == '>' and part[var] > value) or
            (op == '<' and part[var] < value)):
          workflow = dest
          break
      else:
        workflow = workflows[workflow][1]
    if workflow:
      total += sum(part.values())
  return total


def part2(input):
  workflows, _ = input
  total = 0
  ranges = [
      ('in', {'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)})
  ]
  while ranges:
    workflow, part_range = ranges.pop()
    if isinstance(workflow, bool):
      if workflow:
        total += math.prod(x - n + 1 for n, x in part_range.values())
      continue
    for var, op, value, dest in workflows[workflow][0]:
      if op == '>':
        new_range = dict(part_range)
        new_range[var] = (max(part_range[var][0], value + 1),
                          part_range[var][1])
        if new_range[var][0] <= new_range[var][1]:
          ranges.append((dest, new_range))
        part_range[var] = (part_range[var][0], min(part_range[var][1], value))
        if part_range[var][0] > part_range[var][1]:
          break
      elif op == '<':
        new_range = dict(part_range)
        new_range[var] = (part_range[var][0],
                          min(part_range[var][1], value - 1))
        if new_range[var][0] <= new_range[var][1]:
          ranges.append((dest, new_range))
        part_range[var] = (max(part_range[var][0], value), part_range[var][1])
        if part_range[var][0] > part_range[var][1]:
          break
    else:
      ranges.append((workflows[workflow][1], part_range))
  return total


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
