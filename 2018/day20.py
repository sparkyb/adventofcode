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

  return input

DIRS = {
  'N': (-1, 0),
  'S': (1, 0),
  'W': (0, -1),
  'E': (0, 1),
}

def parse(doors, input, index=0, starts=set([(0,0)]), depth=0):
  ## print index, depth, len(starts)
  positions = set(starts)
  ends = set()
  while index < len(input):
    c = input[index]
    if c in DIRS:
      next_positions = set()
      for pos in positions:
        next_pos = (pos[0]+DIRS[c][0],pos[1]+DIRS[c][1])
        doors[pos].add(next_pos)
        doors[next_pos].add(pos)
        next_positions.add(next_pos)
      positions = next_positions
    elif c == '|':
      ends.update(positions)
      positions = set(starts)
    elif c == '(':
      positions, index = parse(doors, input, index + 1, positions, depth+1)
    elif c == ')':
      break
    index += 1
  ends.update(positions)
  return ends, index

def part1(input):
  doors = defaultdict(set)
  parse(doors, input[1:-1])
  distance = {(0,0):0}
  frontier = [(0,0)]
  while frontier:
    pos = frontier.pop(0)
    for next_pos in doors[pos]:
      if next_pos not in distance or distance[pos]+1 < distance[next_pos]:
        distance[next_pos] = distance[pos]+1
        frontier.append(next_pos)
  return max(distance.values())

def part2(input):
  doors = defaultdict(set)
  parse(doors, input[1:-1])
  distance = {(0,0):0}
  frontier = [(0,0)]
  while frontier:
    pos = frontier.pop(0)
    for next_pos in doors[pos]:
      if next_pos not in distance or distance[pos]+1 < distance[next_pos]:
        distance[next_pos] = distance[pos]+1
        frontier.append(next_pos)
  return sum(1 for v in distance.values() if v >= 1000)


if __name__ == '__main__':
  input = get_input()
  print part1(input)
  print part2(input)
