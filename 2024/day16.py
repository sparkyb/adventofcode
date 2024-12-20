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
  return walls, start, end


def part1(input):
  walls, start, end = input
  frontier = [(0, start, (0, 1))]
  scores = {}
  while frontier:
    score, pos, dir = heapq.heappop(frontier)
    if pos == end:
      return score
    for rot in (0, 1, 2, 1):
      next_pos = (pos[0] + dir[0], pos[1] + dir[1])
      if next_pos not in walls:
        next_score = score + 1000 * rot + 1
        if ((next_pos, dir) not in scores or
            scores[(next_pos, dir)] > next_score):
          scores[(next_pos, dir)] = next_score
          heapq.heappush(frontier, (next_score, next_pos, dir))
      dir = (-dir[1], dir[0])
  return None


def part2(input):
  walls, start, end = input
  frontier = [(0, (start,), (0, 1))]
  scores = {}
  min_scores = {}
  on_path = set()
  while frontier:
    score, path, dir = heapq.heappop(frontier)
    pos = path[-1]
    if pos not in min_scores or score == min_scores[pos]:
      min_scores[pos] = score
      if pos == end:
        on_path.update(path)
    for rot in (0, 1, 2, 1):
      next_pos = (pos[0] + dir[0], pos[1] + dir[1])
      if next_pos not in walls:
        next_score = score + 1000 * rot + 1
        if ((next_pos, dir) not in scores or
            scores[(next_pos, dir)] >= next_score):
          scores[(next_pos, dir)] = next_score
          heapq.heappush(frontier, (next_score, path + (next_pos,), dir))
      dir = (-dir[1], dir[0])
  return len(on_path)


# def part2(input):
#   return
#   min_score = part1(input)
#   walls, start, end = input
#   on_path = set()
#   frontier = [(0, (start,), (0, 1))]
#   while frontier:
#     score, path, dir = heapq.heappop(frontier)
#     score = -score
#     pos = path[-1]
#     if pos == end:
#       if score == min_score:
#         on_path.update(path)
#     else:
#       for rot in (0, 1, 2, 1):
#         next_pos = (pos[0] + dir[0], pos[1] + dir[1])
#         next_score = score + 1000 * rot + 1
#         if (next_pos not in walls and next_pos not in path and
#             next_score <= min_score):
#           heapq.heappush(frontier, (-next_score, path + (next_pos,), dir))
#         dir = (-dir[1], dir[0])

#   return len(on_path)


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
