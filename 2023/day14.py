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
  height = len(lines)
  width = len(lines[0])
  board = {
      y: {x: c for x, c in enumerate(line) if c != '.'}
      for y, line in enumerate(lines)
  }
  return board, (height, width)


def transpose(board, size):
  return (
      {
          x: {
              y: c
              for y, line in board.items() for x2, c in line.items() if x2 == x
          }
          for x in range(size[1])
      },
      (size[1], size[0])
  )


def tip(board, size, dir=0):
  last_rock = {}
  new_board = {}
  axis = dir % 2
  sign = dir // 2
  if axis:
    board, size = transpose(board, size)
  for y in range(size[0]):
    if sign:
      y = size[0] - y - 1
    new_board[y] = {}
    for x, c in board[y].items():
      if c == 'O':
        y2 = last_rock.get(x, sign * (size[0] + 1) - 1) - (sign * 2 - 1)
      else:
        y2 = y
      last_rock[x] = y2
      new_board[y2][x] = c
  if axis:
    new_board, size = transpose(new_board, size)
  return new_board


def cycle(board, size):
  for dir in range(4):
    board = tip(board, size, dir)
  return board


def load(board, size):
  return sum((size[0] - y) * sum(c == 'O' for _, c in line.items())
             for y, line in board.items())


def part1(input):
  board, size = input
  return load(tip(board, size), size)


def part2(input):
  board, size = input
  boards = [board]
  n = 1000000000
  for _ in range(n):
    board = cycle(board, size)
    if board in boards:
      offset = boards.index(board)
      length = len(boards) - offset
      board = boards[offset + (n - offset) % length]
      break
    boards.append(board)
  return load(board, size)


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
