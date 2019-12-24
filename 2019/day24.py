import collections
from collections import defaultdict
import enum
import functools
import itertools
import math
import msvcrt
import os.path
import pdb
import re
import sys

import numpy as np

from intcode import Intcode


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  return np.array([list(line) for line in input.split('\n')])


def step(prev):
  next = np.copy(prev)
  kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
  image = np.zeros((prev.shape[0] + 2, prev.shape[1] + 2), dtype=int)
  image[1:-1, 1:-1] = prev == '#'
  for (y, x), cell in np.ndenumerate(next):
    neighbors = np.sum(image[y:y + kernel.shape[0], x:x + kernel.shape[1]] * kernel)
    if cell == '#' and neighbors != 1:
      next[y, x] = '.'
    elif cell == '.' and 1 <= neighbors <= 2:
      next[y, x] = '#'
  return next


def part1(input):
  board = input
  prevs = []
  while tuple(board.flat) not in prevs:
    prevs.append(tuple(board.flat))
    board = step(board)
  return sum(pow(2, i) for i, cell in enumerate(board.flat) if cell == '#')


def step2(prev):
  cy = prev.shape[1] // 2
  cx = prev.shape[2] // 2
  next = np.full((prev.shape[0] + 2, prev.shape[1], prev.shape[2]), '.')
  next[1:-1] = prev
  kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
  image = np.zeros((prev.shape[1] + 2, prev.shape[1] + 2), dtype=int)
  for level in range(next.shape[0]):
    level -= 1
    if 0 <= level < prev.shape[0]:
      image[1:-1, 1:-1] = prev[level] == '#'
    else:
      image[:] = 0
    for (y, x), cell in np.ndenumerate(next[level + 1]):
      if y == cy and x == cx:
        continue
      neighbors = np.sum(image[y:y + kernel.shape[0], x:x + kernel.shape[1]] * kernel)
      if y == 0 and level > 0:
        neighbors += prev[level - 1, cy - 1, cx] == '#'
      if y == prev.shape[1] - 1 and level > 0:
        neighbors += prev[level - 1, cy + 1, cx] == '#'
      if x == 0 and level > 0:
        neighbors += prev[level - 1, cy, cx - 1] == '#'
      if x == prev.shape[2] - 1 and level > 0:
        neighbors += prev[level - 1, cy, cx + 1] == '#'
      if y == cy - 1 and x == cx and level < prev.shape[0] - 1:
        neighbors += sum(prev[level + 1, 0, :] == '#')
      if y == cy + 1 and x == cx and level < prev.shape[0] - 1:
        neighbors += sum(prev[level + 1, -1, :] == '#')
      if y == cy and x == cx - 1 and level < prev.shape[0] - 1:
        neighbors += sum(prev[level + 1, :, 0] == '#')
      if y == cy and x == cx + 1 and level < prev.shape[0] - 1:
        neighbors += sum(prev[level + 1, :, -1] == '#')
      if cell == '#' and neighbors != 1:
        next[level + 1, y, x] = '.'
      elif cell == '.' and 1 <= neighbors <= 2:
        next[level + 1, y, x] = '#'
  return next


def part2(input):
  board = input[None, :]
  for i in range(200):
    board = step2(board)
  return np.sum(board == '#')


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
