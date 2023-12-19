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

  return [[int(c) for c in line] for line in input.split('\n')]


@functools.total_ordering
class State(collections.namedtuple('_State', 'pos dir steps loss')):
  __slots__ = ()

  @property
  def y(self):
    return self.pos[0]

  @property
  def x(self):
    return self.pos[1]

  @property
  def dy(self):
    return self.dir[0]

  @property
  def dx(self):
    return self.dir[1]

  def __lt__(self, other):
    if not isinstance(other, State):
      return NotImplemented
    return self.loss < other.loss


def part1(input, min_steps=0, max_steps=3):
  visited = set()
  frontier = [
    State((1, 0), (1, 0), 1, 0),
    State((0, 1), (0, 1), 1, 0),
  ]
  heapq.heapify(frontier)
  while frontier:
    (y, x), (dy, dx), steps, loss = heapq.heappop(frontier)
    if y < 0 or y >= len(input) or x < 0 or x >= len(input[y]):
      continue
    key = ((y, x), (dy, dx), steps)
    if key in visited:
      continue
    visited.add(key)
    loss += input[y][x]
    if y == len(input) - 1 and x == len(input[y]) - 1:
      return loss
    if steps < max_steps:
      heapq.heappush(frontier,
                     State((y + dy, x + dx), (dy, dx), steps + 1, loss))
    if steps >= min_steps:
      heapq.heappush(frontier, State((y + dx, x + dy), (dx, dy), 1, loss))
      heapq.heappush(frontier, State((y - dx, x - dy), (-dx, -dy), 1, loss))


def part2(input):
  return part1(input, 4, 10)


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
