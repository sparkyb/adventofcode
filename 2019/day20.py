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


class Direction(enum.IntEnum):
  @property
  def delta(self):
    ret = np.array([0, 0])
    ret[self // 2] = (self % 2) * 2 - 1
    return ret

  @property
  def reverse(self):
    return type(self)(self ^ 1)

  @property
  def left(self):
    return type(self)(self ^ (2 | (self // 2)))

  @property
  def right(self):
    return self.left.reverse

  NORTH = 0
  SOUTH = 1
  WEST = 2
  EAST = 3


class Maze:
  def __init__(self, input):
    self.grid = input
    hole = np.array([[31, 31], [84, 86]])
    outside_portals = {}
    for x in range(2, self.grid.shape[1] - 2):
      portal = ''.join(self.grid[0:2, x].flat).strip()
      if portal:
        from_cell = (1, x)
        to_cell = (2, x)
        outside_portals[portal] = (from_cell, to_cell)
      portal = ''.join(self.grid[self.grid.shape[0] - 2:self.grid.shape[0], x].flat).strip()
      if portal:
        from_cell = (self.grid.shape[0] - 2, x)
        to_cell = (self.grid.shape[0] - 3, x)
        outside_portals[portal] = (from_cell, to_cell)
    for y in range(2, self.grid.shape[0] - 2):
      portal = ''.join(self.grid[y, 0:2].flat).strip()
      if portal:
        from_cell = (y, 1)
        to_cell = (y, 2)
        outside_portals[portal] = (from_cell, to_cell)
      portal = ''.join(self.grid[y, self.grid.shape[1] - 2:self.grid.shape[1]].flat).strip()
      if portal:
        from_cell = (y, self.grid.shape[1] - 2)
        to_cell = (y, self.grid.shape[1] - 3)
        outside_portals[portal] = (from_cell, to_cell)
    inside_portals = {}
    for x in range(hole[0, 1], hole[1, 1]):
      portal = ''.join(self.grid[hole[0, 0]:hole[0, 0] + 2, x].flat).strip()
      if portal:
        from_cell = (hole[0, 0], x)
        to_cell = (hole[0, 0] - 1, x)
        inside_portals[portal] = (from_cell, to_cell)
      portal = ''.join(self.grid[hole[1, 0] - 2:hole[1, 0], x].flat).strip()
      if portal:
        from_cell = (hole[1, 0] - 1, x)
        to_cell = (hole[1, 0], x)
        inside_portals[portal] = (from_cell, to_cell)
    for y in range(hole[0, 0], hole[1, 0]):
      portal = ''.join(self.grid[y, hole[0, 1]:hole[0, 1] + 2].flat).strip()
      if portal:
        from_cell = (y, hole[0, 1])
        to_cell = (y, hole[0, 1] - 1)
        inside_portals[portal] = (from_cell, to_cell)
      portal = ''.join(self.grid[y, hole[1, 1] - 2:hole[1, 1]].flat).strip()
      if portal:
        from_cell = (y, hole[1, 1] - 1)
        to_cell = (y, hole[1, 1])
        inside_portals[portal] = (from_cell, to_cell)
    self.start = outside_portals.pop('AA')[1]
    self.end = outside_portals.pop('ZZ')[1]
    self.portals = {}
    assert outside_portals.keys() == inside_portals.keys()
    for portal in outside_portals:
      self.portals[outside_portals[portal][0]] = (inside_portals[portal][1], -1)
      self.portals[inside_portals[portal][0]] = (outside_portals[portal][1], 1)

  def bfs(self, levels):
    liberties = collections.deque([(self.start, 0)])
    distances = {(self.start, 0): 0}

    while liberties:
      pos, level = liberties.popleft()
      for dir in Direction:
        new_pos = tuple(np.array(pos) + dir.delta)
        new_level = level
        if new_pos in self.portals:
          new_pos, delta_level = self.portals[new_pos]
          if levels:
            new_level += delta_level
            if new_level < 0:
              continue
        if (new_pos, new_level) in distances:
          continue
        cell = self.grid[new_pos]
        if cell != '.':
          continue
        distances[(new_pos, new_level)] = distances[(pos, level)] + 1
        liberties.append((new_pos, new_level))
        if new_pos == self.end and new_level == 0:
          return distances[(new_pos, new_level)]


def part1(input):
  maze = Maze(input)
  return maze.bfs(False)


def part2(input):
  maze = Maze(input)
  return maze.bfs(True)


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
