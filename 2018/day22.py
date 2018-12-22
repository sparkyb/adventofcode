import os.path
import re
import math
from collections import defaultdict
import itertools
import md5
import msvcrt
import sys


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0]+'.txt'
  with open(filename) as fp:
    input = fp.read().rstrip()

  lines = input.split('\n')
  depth = int(re.search(r'^depth: (\d+)$', lines[0]).group(1))
  target = map(int, re.search(r'^target: (\d+),(\d+)$', lines[1]).groups())
  return depth, target

INDEX_CACHE = {}

def geologic_index(x, y, depth, target):
  if (x, y) not in INDEX_CACHE:
    if x == 0 and y == 0:
      index = 0
    elif x == target[0] and y == target[1]:
      index = 0
    elif y == 0:
      index = x * 16807
    elif x == 0:
      index = y * 48271
    else:
      index = erosion_level(x - 1, y, depth, target) * erosion_level(x, y - 1, depth, target)
    INDEX_CACHE[(x, y)] = index
  return INDEX_CACHE[(x, y)]

EROSION_CACHE = {}

def erosion_level(x, y, depth, target):
  if (x, y) not in EROSION_CACHE:
    EROSION_CACHE[(x, y)] = (geologic_index(x, y, depth, target) + depth) % 20183
  return EROSION_CACHE[(x, y)]

def terrain_type(x, y, depth, target):
  return erosion_level(x, y, depth, target) % 3

ROCKY = 0
WET = 1
NARROW = 2

TORCH = frozenset([ROCKY, NARROW])
CLIMBING_GEAR = frozenset([ROCKY, WET])
NEITHER = frozenset([WET, NARROW])

TOOLS = {
  ROCKY: set([TORCH, CLIMBING_GEAR]),
  WET: set([CLIMBING_GEAR, NEITHER]),
  NARROW: set([TORCH, NEITHER]),
}

def switch_tool(terrain, tool):
  return list(TOOLS[terrain] - set([tool]))[0]

def astar_all(start, goal_func, neighbors_func, heuristic_func):
  explored = set()
  frontier = [start]
  g = {start: 0}
  h = {start: heuristic_func(start)}
  f = {start: h[start]}
  while frontier:
    current = frontier.pop(0)
    explored.add(current)
    if goal_func(current):
      yield current, g[current]
      continue
    for neighbor, distance in neighbors_func(current):
      if neighbor in explored:
        continue
      distance += g[current]
      if neighbor not in frontier:
        frontier.append(neighbor)
        g[neighbor] = distance
        h[neighbor] = heuristic_func(neighbor)
        f[neighbor] = distance + h[neighbor]
      elif distance < g[neighbor]:
        g[neighbor] = distance
        f[neighbor] = distance + h[neighbor]
    frontier.sort(key=lambda node: (f[node],h[node]))

def astar(start, goal_func, neighbors_func, heuristic_func):
  for result in astar_all(start, goal_func, neighbors_func, heuristic_func):
    return result
  return None

def bfs(start, goal_func, neighbors_func):
  explored = set()
  frontier = [start]
  g = {start: 0}
  while frontier:
    current = frontier.pop(0)
    explored.add(current)
    if goal_func(current):
      return current, g[current]
    for neighbor, distance in neighbors_func(current):
      if neighbor in explored:
        continue
      distance += g[current]
      if neighbor not in frontier:
        frontier.append(neighbor)
        g[neighbor] = distance
      elif distance < g[neighbor]:
        g[neighbor] = distance
    frontier.sort(key=lambda node: g[node])

def neighbors(depth, target):
  def wrapper(state):
    x, y, tool = state
    dirs = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    for dx, dy in dirs:
      if x + dx < 0 or y + dy < 0:
        continue
      terrain = terrain_type(x + dx, y + dy, depth, target)
      if terrain not in tool:
        continue
      yield (x + dx, y + dy, tool), 1
    terrain = terrain_type(x, y, depth, target)
    yield (x, y, switch_tool(terrain, tool)), 7
  return wrapper

def heuristic(target):
  def wrapper(state):
    x, y, tool = state
    return abs(target[0] - x) + abs(target[1] - y) + (7 if tool != TORCH else 0)
  return wrapper

def goal(target):
  def wrapper(state):
    x, y, tool = state
    return x == target[0] and y == target[1] and tool == TORCH
  return wrapper

def part1(input):
  depth, target = input
  risk = 0
  for y in xrange(target[1] + 1):
    for x in xrange(target[0] + 1):
      risk += terrain_type(x, y, depth, target)
  return risk

def part2(input):
  depth, target = input
  start = (0, 0, TORCH)
  return astar(start, goal(target), neighbors(depth, target), heuristic(target))[1]
  ## return bfs(start, goal(target), neighbors(depth, target))[1]


if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser(usage='%prog [options] [<input.txt>]')
  options, args = parser.parse_args()
  input = get_input(*args)
  print part1(input)
  print part2(input)
