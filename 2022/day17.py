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

  return [-1 if c == '<' else 1 for c in input]


ROCKS = [
    {(0, 0), (0, 1), (0, 2), (0, 3)},
    {(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)},
    {(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)},
    {(0, 0), (1, 0), (2, 0), (3, 0)},
    {(0, 0), (0, 1), (1, 0), (1, 1)},
]


def move_rock(rock, dy=0, dx=0):
  return {(y + dy, x + dx) for y, x in rock}


def can_move(pit, rock):
  return all(y >= 0 and 0 <= x < 7 for y, x in rock) and not (pit & rock)


def draw_pit(pit, height, rock=frozenset()):
  if rock:
    height = max(height, max(y for y, _ in rock) + 1)
  for y in range(height - 1, -1, -1):
    print('|{}|'.format(''.join(
        '@' if (y, x) in rock else '#' if (y, x) in pit else '.'
        for x in range(7))))
  print('+-------+')
  print()


def trim_pit(pit, height):
  min_y = height
  visited = set()
  frontier = collections.deque([(height - 1, x) for x in range(7)
                                if (height - 1, x) not in pit and height])
  while frontier:
    y, x = frontier.popleft()
    if (y, x) in visited or (y, x) in pit or y < 0 or x < 0 or x >= 7:
      continue
    visited.add((y, x))
    min_y = min(min_y, y)
    frontier.extend([(y + dy, x + dx) for dy, dx in [(-1, 0), (0, -1), (0, 1)]])
  if min_y:
    pit = {(y - min_y, x) for y, x in pit if y >= min_y}
  return pit, min_y


def drop_rock(pit, height, rock, wind, windex):
  rock = move_rock(ROCKS[rock % len(ROCKS)], height + 3, 2)
  new_rock = rock
  while can_move(pit, new_rock):
    rock = new_rock
    ## draw_pit(pit, height, rock)
    ## if msvcrt.getch() == b'\x1b':
      ## sys.exit(0)
    new_rock = move_rock(rock, 0, wind[windex])
    windex = (windex + 1) % len(input)
    if can_move(pit, new_rock):
      rock = new_rock
    ## draw_pit(pit, height, rock)
    ## if msvcrt.getch() == b'\x1b':
      ## sys.exit(0)
    new_rock = move_rock(rock, -1)
  pit |= rock
  height = max(height, max(y for y, _ in rock) + 1)
  pit, offset = trim_pit(pit, height)
  return pit, height - offset, offset, windex


def drop_rocks(wind, rocks):
  pit = set()
  offset = 0
  height = 0
  windex = 0
  prev_states = {(frozenset(), 0, 0): (0, 0)}
  rock = 0
  while rock < rocks:
    pit, height, shift, windex = drop_rock(pit, height, rock, wind, windex)
    offset += shift
    rock += 1
    state = (frozenset(pit), rock % len(ROCKS), windex)
    if state in prev_states:
      prev_rock, prev_offset = prev_states[state]
      n = (rocks - prev_rock) // (rock - prev_rock)
      rock = prev_rock + n * (rock - prev_rock)
      offset = prev_offset + n * (offset - prev_offset)
      break
    else:
      prev_states[state] = (rock, offset)
  while rock < rocks:
    pit, height, shift, windex = drop_rock(pit, height, rock, wind, windex)
    offset += shift
    rock += 1
  return offset + height


def part1(input):
  return drop_rocks(input, 2022)


def part2(input):
  return drop_rocks(input, 1000000000000)


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
