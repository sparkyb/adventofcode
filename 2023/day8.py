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

  directions, network = input.split('\n\n')
  directions = ['LR'.index(c) for c in directions]
  network = {src: (l, r) for src, l, r in [
      re.search(r'^(\w{3}) = \((\w{3}), (\w{3})\)$', line).groups()
      for line in network.split('\n')
  ]}
  return directions, network


def part1(input):
  directions, network = input
  loc = 'AAA'
  steps = 0
  while loc != 'ZZZ':
    loc = network[loc][directions[steps % len(directions)]]
    steps += 1
  return steps


def find_cycle(directions, network, start):
  visited = set()
  step = 0
  loc = start
  path = []
  while (step, loc) not in visited:
    visited.add((step, loc))
    path.append((step, loc))
    loc = network[loc][directions[step]]
    step = (step + 1) % len(directions)
  prefix = path.index((step, loc))
  ends = [i for i, (_, loc) in enumerate(path) if loc[-1] == 'Z']
  return prefix, len(path) - prefix, ends


def crt(end_steps):
  gcd = math.gcd(*(n for _, n in end_steps))
  lcm = math.lcm(*(n for _, n in end_steps))
  total = end_steps[0][0] * pow(lcm // gcd, -1, gcd) * lcm // gcd
  for a, n in end_steps:
    n //= gcd
    total += a * pow(lcm // n, -1, n) * lcm // n
  return total % lcm


def part2(input):
  directions, network = input
  cycles = [find_cycle(directions, network, loc)
            for loc in network if loc[-1] == 'A']
  for prefix, loop, ends in cycles:
    assert all(end >= prefix for end in ends)
  max_prefix = max(prefix for prefix, _, _ in cycles)
  cycles = [
      (loop, [(end - max_prefix) % loop for end in ends])
      for prefix, loop, ends in cycles
  ]
  min_steps = None
  for end_steps in itertools.product(
      *([(end, loop) for end in ends] for loop, ends in cycles)):
    if not all(a1 % math.gcd(n1, n2) == a2 % math.gcd(n1, n2)
               for (a1, n1), (a2, n2) in itertools.combinations(end_steps, 2)):
      continue
    steps = max_prefix + crt(end_steps)
    if min_steps is None or steps < min_steps:
      min_steps = steps
  return min_steps


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
