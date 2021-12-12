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

  edges = collections.defaultdict(set)
  for a, b in (line.split('-') for line in input.split('\n')):
    edges[a].add(b)
    edges[b].add(a)
  return edges


def is_small(cave):
  return cave.islower()


def paths(edges, small2=False):
  @functools.lru_cache(maxsize=None)
  def traverse(path, small2=True):
    count = 0
    for cave in edges[path[-1]]:
      if cave == 'end':
        count += 1
      elif (cave != 'start' and
            (small2 or not is_small(cave) or cave not in path)):
        count += traverse(
            path + (cave,),
            small2=small2 and (not is_small(cave) or cave not in path))
    return count

  return traverse(('start',), small2=small2)


def part1(edges):
  return paths(edges, small2=False)


def part2(edges):
  return paths(edges, small2=True)


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
