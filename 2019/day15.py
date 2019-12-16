from collections import defaultdict
import enum
import itertools
import math
from hashlib import md5
import msvcrt
import numpy as np
import os.path
import re
import sys

from intcode import Intcode


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip()

  return list(map(int, input.split(',')))


class Direction(enum.IntEnum):
  @property
  def delta(self):
    ret = np.array([0, 0])
    ret[(self - 1) // 2] = ((self - 1) % 2) * 2 - 1
    return ret

  @property
  def reverse(self):
    return type(self)(((self - 1) ^ 1) + 1)

  @property
  def left(self):
    return type(self)(((self - 1) ^ (2 | ((self - 1) // 2))) + 1)

  @property
  def right(self):
    return self.left.reverse

  NORTH = 1
  SOUTH = 2
  WEST = 3
  EAST = 4

  def __str__(self):
    return self.name[0]


class Cell(enum.IntEnum):
  def __new__(cls, status, char):
    member = int.__new__(cls, status)
    member._value_ = status
    return member

  def __init__(self, status, char):
    self.char = char

  START = (-1, '+')
  WALL = (0, '#')
  EMPTY = (1, '.')
  OXYGEN = (2, 'O')


class Path(list):
  @property
  def position(self):
    return tuple(sum((dir.delta for dir in self), np.array([0,0])))

  @property
  def reverse(self):
    return type(self)(dir.reverse for dir in reversed(self))

  def __getitem__(self, index):
    ret = super().__getitem__(index)
    if isinstance(index, slice):
      ret = type(self)(ret)
    return ret

  def __add__(self, other):
    return type(self)(super().__add__(other))

  def path_to(self, target):
    index = 0
    while (index < len(self) and index < len(target) and
           self[index] == target[index]):
      index += 1
    return self[index:].reverse + target[index:]


class Maze:
  def __init__(self, input):
    self.prog = Intcode(input)
    self.reset()

  @property
  def position(self):
    return self.path.position

  def reset(self):
    self.path = Path([])
    self.paths = {self.position: Path(self.path)}
    self.cells = {self.position: Cell.START}
    self.oxygen = None
    self.liberties = {}
    self.update_liberties()

  def visited(self, pos):
    return pos in self.cells

  def update_liberties(self):
    for dir in Direction:
      neighbor = self.path + [dir]
      pos = neighbor.position
      if not self.visited(pos):
        if pos not in self.liberties or len(neighbor) < len(self.liberties[pos]):
          self.liberties[pos] = neighbor

  def move(self, dir, blind=False):
    dir = Direction(dir)
    self.prog.input.append(int(dir))
    status = Cell(self.prog.run(True))
    if status:
      if self.path and self.path[-1].reverse == dir:
        self.path.pop()
      else:
        self.path.append(dir)
      if not blind:
        pos = self.position
        if not self.visited(pos) or len(self.path) < len(self.paths[pos]):
          self.paths[pos] = Path(self.path)
          self.cells[pos] = status
          if status == Cell.OXYGEN:
            self.oxygen = self.position
          self.update_liberties()
      return True
    else:
      self.cells[(self.path + [dir]).position] = status
      return False

  def goto(self, path):
    if not isinstance(path, Path) and path in self.paths:
      path = self.paths[path]
    for dir in self.path.path_to(path):
      self.move(dir)

  def explore(self, depth_first=True, stop_at_oxygen=False):
    while self.liberties and (not stop_at_oxygen or self.oxygen is None):
      target = sorted(self.liberties, key=lambda pos: len(self.liberties[pos]),
                      reverse=depth_first)[0]
      self.goto(self.liberties.pop(target))

  def wall_follow(self, stop_at_oxygen=False):
    dir = Direction.NORTH
    while not stop_at_oxygen or self.oxygen is None:
      for try_dir in [dir.left, dir, dir.right, dir.reverse]:
        if self.move(try_dir):
          if not self.path:
            return
          dir = try_dir
          break

  def draw_map(self):
    min_y = min(pos[0] for pos in self.cells)
    max_y = max(pos[0] for pos in self.cells)
    min_x = min(pos[1] for pos in self.cells)
    max_x = max(pos[1] for pos in self.cells)
    grid = np.full((max_y - min_y + 1, max_x - min_x + 1), ' ')
    for pos, status in self.cells.items():
      grid[pos[0] - min_y, pos[1] - min_x] = status.char
    for line in grid:
      print(''.join(line))


def part1(input):
  maze = Maze(input)
  maze.explore(depth_first=True, stop_at_oxygen=True)
  ## maze.wall_follow(stop_at_oxygen=True)
  maze.draw_map()
  return len(maze.paths[maze.oxygen])


def part2(input):
  maze = Maze(input)
  maze.explore(depth_first=True, stop_at_oxygen=True)
  ## maze.wall_follow(stop_at_oxygen=True)
  ## maze.goto(maze.oxygen)
  maze.reset()
  maze.explore(depth_first=True, stop_at_oxygen=False)
  ## maze.wall_follow(stop_at_oxygen=False)
  return max(len(path) for path in maze.paths.values())


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
