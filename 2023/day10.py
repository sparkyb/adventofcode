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
      (y, x): c
      for y, line in enumerate(input.split('\n'))
      for x, c in enumerate(line)
      if c != '.'
  }


class Pipe(tuple):
  def transform(self, entrance):
    exit = self[1 - self.index(entrance)]
    return (-exit[0], -exit[1])


PIPES = {
    '|': Pipe(((1, 0), (-1, 0))),
    '-': Pipe(((0, 1), (0, -1))),
    'F': Pipe(((-1, 0), (0, -1))),
    '7': Pipe(((0, 1), (-1, 0))),
    'J': Pipe(((1, 0), (0, 1))),
    'L': Pipe(((1, 0), (0, -1))),
}


def find_start(input):
  for (y, x), c in input.items():
    if c == 'S':
      return (y, x)


def traverse_loop(input, start, direction):
  y, x = start
  dy, dx = direction
  loop_tiles = {(y, x)}
  y += dy
  x += dx
  while input[(y, x)] != 'S':
    loop_tiles.add((y, x))
    dy, dx = PIPES[input[(y, x)]].transform((dy, dx))
    y += dy
    x += dx
  return loop_tiles, (dy, dx)


def part1(input):
  start = find_start(input)
  for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    try:
      return len(traverse_loop(input, start, direction)[0]) // 2
    except KeyError:
      pass


def draw_grid(input, inside_tiles, loop_tiles):
  max_y = max(y for y, _ in input)
  max_x = max(x for _, x in input)
  for y in range(max_y + 1):
    print(''.join('I' if (y, x) in inside_tiles else (input.get((y, x), '.') if loop_tiles and (y, x) in loop_tiles else '.') for x in range(max_x + 1)))


def part2(input):
  start = find_start(input)
  for start_direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    try:
      loop_tiles, end_direction = traverse_loop(input, start, start_direction)
    except KeyError:
      pass
    else:
      start_direction = (-start_direction[0], -start_direction[1])
      for c, pipe in PIPES.items():
        if start_direction in pipe and end_direction in pipe:
          input[start] = c
          break
      else:
        raise ValueError
      break
  else:
    raise ValueError

  min_y = min(y for y, _ in loop_tiles)
  max_y = max(y for y, _ in loop_tiles)
  min_x = min(x for _, x in loop_tiles)
  max_x = max(x for _, x in loop_tiles)

  inside_tiles = 0
  for y in range(min_y + 1, max_y):
    inside = False
    last_corner = None
    for x in range(min_x, max_x):
      if (y, x) in loop_tiles:
        if input[(y, x)] == '|':
          assert last_corner is None
          inside = not inside
        elif input[(y, x)] in 'FL':
          assert last_corner is None
          last_corner = 'FL'.index(input[(y, x)])
        elif input[(y, x)] in 'J7':
          assert last_corner is not None
          if 'J7'.index(input[(y, x)]) == last_corner:
            inside = not inside
          last_corner = None
        else:
          assert last_corner is not None and input[(y, x)] == '-'
      elif inside:
        inside_tiles += 1
  return inside_tiles


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
