import collections
from collections import defaultdict
import enum
import functools
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

  def __str__(self):
    return self.name[0]


class Maze:
  def __init__(self, input):
    self.grid = input
    self.start = [tuple(pos) for pos in np.argwhere(self.grid == '@')]
    self.keys = {}
    for y, row in enumerate(self.grid):
      for x, cell in enumerate(row):
        if 'a' <= cell <= 'z':
          self.keys[cell] = (y, x)
    self.adjacent = defaultdict(set)
    self.distances = {}
    self.doors = {}
    for start_pos in self.start:
      self.find_keys(start_pos)
      self.fill_distances([start_pos])
    for key_pos in self.keys.values():
      self.fill_distances([key_pos])

  def find_keys(self, start_pos):
    found_keys = {}
    liberties = collections.deque([(start_pos, frozenset())])
    distances = {start_pos: 0}
    while liberties:
      pos, doors = liberties.popleft()
      for dir in Direction:
        new_pos = tuple(np.array(pos) + dir.delta)
        if new_pos in distances:
          continue
        cell = self.grid[new_pos]
        if cell == '#':
          continue
        new_doors = doors
        if 'A' <= cell <= 'Z':
          new_doors = doors | frozenset([cell.lower()])
        distances[new_pos] = distances[pos] + 1
        if 'a' <= cell <= 'z':
          self.adjacent[start_pos].add(cell)
          self.distances[(start_pos, new_pos)] = distances[new_pos]
          self.doors[(start_pos, new_pos)] = new_doors
          if new_pos not in self.adjacent:
            self.find_keys(new_pos)
        else:
          liberties.append((new_pos, new_doors))

  def fill_distances(self, chain, distance=0, doors=frozenset()):
    if len(chain) > 1:
      if (chain[0], chain[-1]) not in self.distances or distance < self.distances[(chain[0], chain[-1])]:
        self.distances[(chain[0], chain[-1])] = distance
        self.doors[(chain[0], chain[-1])] = doors
    for key in self.adjacent[chain[-1]]:
      key_pos = self.keys[key]
      if key_pos in chain:
        continue
      self.fill_distances(chain + [key_pos], distance + self.distances[(chain[-1], key_pos)],
                          doors | self.doors[(chain[-1], key_pos)])

  def reachable(self, start_pos, have_keys):
    found_keys = set()
    explored = set([start_pos])
    adjacent_keys = collections.deque(self.adjacent[start_pos])
    while adjacent_keys:
      key = adjacent_keys.popleft()
      key_pos = self.keys[key]
      if key_pos in explored:
        continue
      if not (self.doors[(start_pos, key_pos)] <= have_keys):
        continue
      if key in have_keys:
        explored.add(key_pos)
        adjacent_keys.extend(self.adjacent[key_pos])
      else:
        found_keys.add(key)
    return found_keys

  def shortest_path(self, bots=None, have_keys=None, memo={}):
    if bots is None:
      bots = self.start
    bots = frozenset(bots)
    if have_keys is None:
      have_keys = []
    memo_key = (bots, frozenset(have_keys))
    if memo_key in memo:
      return memo[memo_key]
    shortest = None
    for bot in bots:
      keys = self.reachable(bot, set(have_keys))
      for key in keys:
        key_pos = self.keys[key]
        distance = self.distances[(bot, key_pos)]
        if shortest is not None and distance >= shortest:
          continue
        new_bots = bots - set([bot]) | set([key_pos])
        distance += self.shortest_path(new_bots, have_keys + [key])
        if shortest is None or distance < shortest:
          shortest = distance
    if shortest is None:
      shortest = 0
    memo[memo_key] = shortest
    return shortest


def part1(input):
  print('Building maze...')
  maze = Maze(input)
  print('Finding shortest path...')
  return maze.shortest_path()


def part2(input):
  print('Building maze...')
  grid = np.copy(input)
  start = np.argwhere(grid == '@')[0]
  grid[start[0] - 1:start[0] + 2, start[1] - 1:start[1] + 2] = (
      np.array([['@', '#', '@'], ['#', '#', '#'], ['@', '#', '@']]))
  maze = Maze(grid)
  print('Finding shortest path...')
  return maze.shortest_path()
  return None


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
