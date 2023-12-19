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

  return [({(y, x) for y, line in enumerate(board)
            for x, c in enumerate(line) if c == '#'},
           (len(board), len(board[0])))
          for board in (board.split('\n') for board in input.split('\n\n'))]


def split_y(board, y, height):
  max_y = min(y, height - y)
  top = {(y - y2 - 1, x2) for y2, x2 in board if y2 < y and y - y2 - 1 < max_y}
  bottom = {(y2 - y, x2) for y2, x2 in board if y2 >= y and y2 - y < max_y}
  return top, bottom


def split_x(board, x, width):
  max_x = min(x, width - x)
  left = {(y2, x - x2 - 1) for y2, x2 in board if x2 < x and x - x2 - 1 < max_x}
  right = {(y2, x2 - x) for y2, x2 in board if x2 >= x and x2 - x < max_x}
  return left, right


def find_reflection(board, height, width, ignore=0):
  for y in range(1, height):
    top, bottom = split_y(board, y, height)
    if top == bottom and ignore != 100 * y:
      return 100 * y
  for x in range(1, width):
    left, right = split_x(board, x, width)
    if left == right and ignore != x:
      return x
  raise ValueError


def part1(input):
  return sum(find_reflection(board, height, width)
             for board, (height, width) in input)


def part2(input):
  total = 0
  for board, (height, width) in input:
    prev_value = find_reflection(board, height, width)
    for y in range(height):
      for x in range(width):
        new_board = set(board)
        if (y, x) in board:
          new_board.remove((y, x))
        else:
          new_board.add((y, x))
        try:
          new_value = find_reflection(new_board, height, width,
                                      ignore=prev_value)
        except ValueError:
          pass
        else:
          total += new_value
          break
      else:
        continue
      break
    else:
      raise ValueError
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
