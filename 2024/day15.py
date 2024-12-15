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


DIRS = {
  '<': (0, -1),
  '>': (0, 1),
  '^': (-1, 0),
  'v': (1, 0),
}


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  grid, moves = input.split('\n\n')
  grid = {(y, x): c for y, row in enumerate(grid.split('\n'))
          for x, c in enumerate(row) if c != '.'}
  for pos, c in grid.items():
    if c == '@':
      robot = pos
      break
  del grid[robot]
  moves = [DIRS[c] for c in moves.replace('\n', '')]
  return grid, robot, moves


def do_move(grid, robot, move):
  next_robot = (robot[0] + move[0], robot[1] + move[1])
  y, x = next_robot
  if move[1]:
    while (y, x) in grid:
      if grid[(y, x)] == '#':
        return robot
      x += move[1]
    while x != next_robot[1]:
      grid[(y, x)] = grid.pop((y, x - move[1]))
      x -= move[1]
    return next_robot
  else:
    if (y, x) not in grid:
      return next_robot
    elif grid[(y, x)] == '#':
      return robot
    boxes = []
    if grid[(y, x)] == '[':
      boxes.append({x, x + 1})
    elif grid[(y, x)] == ']':
      boxes.append({x - 1, x})
    else:
      boxes.append({x})
    y += move[0]
    while any((y, x) in grid for x in boxes[-1]):
      if any(grid.get((y, x)) == '#' for x in boxes[-1]):
        return robot
      next_row = set()
      for x in boxes[-1]:
        if (y, x) not in grid:
          continue
        if grid[(y, x)] == '[':
          next_row.update({x, x + 1})
        elif grid[(y, x)] == ']':
          next_row.update({x - 1, x})
        else:
          next_row.add(x)
      boxes.append(next_row)
      y += move[0]
    for row in reversed(boxes):
      for x in row:
        grid[(y, x)] = grid.pop((y - move[0], x))
      y -= move[0]
    return next_robot


def part1(input):
  grid, robot, moves = input
  grid = dict(grid)
  for move in moves:
    robot = do_move(grid, robot, move)
  return sum(y * 100 + x for (y, x), c in grid.items() if c == 'O')


def part2(input):
  grid, robot, moves = input
  wide_grid = {}
  for (y, x), c in grid.items():
    if c == '#':
      wide_grid[(y, x * 2)] = '#'
      wide_grid[(y, x * 2 + 1)] = '#'
    else:
      wide_grid[(y, x * 2)] = '['
      wide_grid[(y, x * 2 + 1)] = ']'
  grid = wide_grid
  robot = (robot[0], robot[1] * 2)
  for move in moves:
    robot = do_move(grid, robot, move)
  return sum(y * 100 + x for (y, x), c in grid.items() if c == '[')


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
