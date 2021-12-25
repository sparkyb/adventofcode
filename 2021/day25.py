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

  lines = input.split('\n')
  return (
      (len(lines), len(lines[0])),
      {(y, x): d
       for y, line in enumerate(lines)
       for x, d in enumerate(line) if d in 'v>'},
  )



def step(board, size):
  board = dict(board)
  east = [(y, x) for (y, x), d in board.items()
          if d == '>' and (y, (x + 1) % size[1]) not in board]
  for y, x in east:
    board[(y, (x + 1) % size[1])] = board.pop((y, x))
  south = [(y, x) for (y, x), d in board.items()
           if d == 'v' and ((y + 1) % size[0], x) not in board]
  for y, x in south:
    board[((y + 1) % size[0], x)] = board.pop((y, x))
  return board


def print_board(board, size):
  for y in range(size[0]):
    print(''.join(board.get((y, x), '.') for x in range(size[1])))


def part1(input):
  size, board = input
  i = 0
  while True:
    i += 1
    new_board = step(board, size)
    if new_board == board:
      return i
    board = new_board


def part2(input):
  return None


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
