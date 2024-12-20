#!/usr/bin/env python

import collections
from collections import defaultdict
import enum
import functools
import heapq
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

  walls = set()
  start = None
  end = None
  for y, row in enumerate(input.split('\n')):
    for x, c in enumerate(row):
      if c == 'S':
        start = (y, x)
      elif c == 'E':
        end = (y, x)
      elif c == '#':
        walls.add((y, x))
  return start, end, walls


def calc_distances(start, walls):
  frontier = [(0, start)]
  distances = {}
  while frontier:
    dist, pos = heapq.heappop(frontier)
    if pos in distances:
      continue
    distances[pos] = dist
    for dir in ((-1, 0), (1, 0), (0, -1), (0, 1)):
      new_pos = (pos[0] + dir[0], pos[1] + dir[1])
      if new_pos not in walls and new_pos not in distances:
        heapq.heappush(frontier, (dist + 1, new_pos))
  return distances


def part1(input):
  start, end, walls = input
  from_start = calc_distances(start, walls)
  from_end = calc_distances(end, walls)
  base_dist = from_start[end]
  count = 0
  for wall in walls:
    for dir in ((-1, 0), (1, 0), (0, -1), (0, 1)):
      before = (wall[0] - dir[0], wall[1] - dir[1])
      after = (wall[0] + dir[0], wall[1] + dir[1])
      if before in from_start and after in from_end:
        dist = from_start[before] + from_end[after] + 2
        if base_dist - dist >= 100:
          count += 1
  return count


def part2(input):
  start, end, walls = input
  from_start = calc_distances(start, walls)
  from_end = calc_distances(end, walls)
  base_dist = from_start[end]
  deltas = {}
  frontier = [(0, (0, 0))]
  while frontier:
    dist, pos = heapq.heappop(frontier)
    if pos in deltas:
      continue
    deltas[pos] = dist
    for dir in ((-1, 0), (1, 0), (0, -1), (0, 1)):
      new_pos = (pos[0] + dir[0], pos[1] + dir[1])
      if new_pos not in deltas and dist < 20:
        heapq.heappush(frontier, (dist + 1, new_pos))
  count = 0
  for before, before_dist in from_start.items():
    if from_end[before] <= 100:
      continue
    for delta, between_dist in deltas.items():
      after = (before[0] + delta[0], before[1] + delta[1])
      if after not in from_end:
        continue
      dist = before_dist + between_dist + from_end[after]
      if base_dist - dist >= 100:
        count += 1
  return count


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
