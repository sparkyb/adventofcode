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

  return {
      (y, x)
      for y, line in enumerate(input.split('\n'))
      for x, c in enumerate(line)
      if c == '#'
  }


DIRECTIONS = [
    ((-1, 0), (-1, -1), (-1, 1)),
    ((1, 0), (1, -1), (1, 1)),
    ((0, -1), (-1, -1), (1, -1)),
    ((0, 1), (-1, 1), (1, 1)),
]


def calculate_move(elves, elf, directions):
  y, x = elf
  for dy,  dx in itertools.product((-1, 0, 1), repeat=2):
    if dx == 0 and dy == 0:
      continue
    if (y + dy, x + dx) in elves:
      break
  else:
    return None
  for dir in directions:
    for dy, dx in dir:
      if (y + dy, x + dx) in elves:
        break
    else:
      return (y + dir[0][0], x + dir[0][1])
  return (y, x)


def do_round(elves, directions):
  moves = collections.defaultdict(set)
  for elf in elves:
    moves[calculate_move(elves, elf, directions)].add(elf)
  new_elves = set()
  for dest, sources in moves.items():
    if dest is None or len(sources) > 1:
      new_elves.update(sources)
    else:
      new_elves.add(dest)
  if None in moves and len(moves) == 1:
    return None
  return new_elves


def draw_grid(elves):
  min_y = min(y for y, _ in elves)
  min_x = min(x for _, x in elves)
  max_y = max(y for y, _ in elves)
  max_x = max(x for _, x in elves)
  for y in range(min_y, max_y + 1):
    print(''.join('#' if (y, x) in elves else '.'
                  for x in range(min_x, max_x + 1)))
  print()


def part1(input):
  directions = collections.deque(DIRECTIONS)
  elves = input
  for _ in range(10):
    ## draw_grid(elves)
    ## if msvcrt.getch() == b'\x1b':
      ## sys.exit(0)
    elves = do_round(elves, directions)
    assert elves
    directions.rotate(-1)
  ## draw_grid(elves)
  min_y = min(y for y, _ in elves)
  min_x = min(x for _, x in elves)
  max_y = max(y for y, _ in elves)
  max_x = max(x for _, x in elves)
  return (max_y - min_y + 1) * (max_x - min_x + 1) - len(elves)


def part2(input):
  directions = collections.deque(DIRECTIONS)
  elves = input
  round = 0
  while elves:
    round += 1
    elves = do_round(elves, directions)
    directions.rotate(-1)
  return round


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
