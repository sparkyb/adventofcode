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

import numpy as np


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  sections = input.split('\n\n')
  numbers = list(map(int, sections[0].split(',')))
  boards = [np.array([list(map(int, line.strip().split()))
                      for line in section.split('\n')])
            for section in sections[1:]]
  return numbers, boards


def is_solved(board, numbers):
  covered = np.isin(board, numbers)
  return np.any(np.all(covered, axis=0)) or np.any(np.all(covered, axis=1))


def score_board(board, numbers):
  return np.sum(board, where=np.isin(board, numbers, invert=True)) * numbers[-1]


def part1(input):
  numbers, boards = input
  for i in range(5, len(numbers) + 1):
    for board in boards:
      if is_solved(board, numbers[:i]):
        return score_board(board, numbers[:i])
  return None


def part2(input):
  numbers, boards = input
  for i in range(len(numbers), 4, -1):
    for board in boards:
      if not is_solved(board, numbers[:i]):
        return score_board(board, numbers[:i + 1])
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
