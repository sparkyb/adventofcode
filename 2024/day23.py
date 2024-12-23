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

  pairs = [tuple(connection.split('-')) for connection in input.split('\n')]
  connections = collections.defaultdict(set)
  for a, b in pairs:
    connections[a].add(b)
    connections[b].add(a)
  return connections


def part1(connections):
  cliques = set()
  for a, neighbors in connections.items():
    if not a.startswith('t'):
      continue
    for b, c in itertools.combinations(neighbors, 2):
      if c in connections[b]:
        cliques.add(frozenset({a, b, c}))
  return len(cliques)


def part2(connections):
  largest = set()
  for a, neighbors in connections.items():
    for n in range(len(neighbors), len(largest), -1):
      if n <= len(largest):
        break
      for clique in itertools.combinations(neighbors, n - 1):
        clique = set(clique) | {a}
        if all(clique - connections[b] == {b} for b in clique):
          largest = clique
          break
  return ','.join(sorted(largest))


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
