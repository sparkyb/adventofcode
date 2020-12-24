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

  return [re.findall(r'e|w|se|sw|ne|nw', line) for line in input.split('\n')]


DIRS = {
    'e': (0, 2),
    'w': (0, -2),
    'ne': (-1, 1), 
    'nw': (-1, -1), 
    'se': (1, 1), 
    'sw': (1, -1), 
}


def part1(input):
  black_tiles = set()
  for dirs in input:
    coord = (0, 0)
    for dir in dirs:
      coord = (coord[0] + DIRS[dir][0], coord[1] + DIRS[dir][1])
    black_tiles ^= {coord}
  return len(black_tiles)


def neighbors(coord):
  return {(coord[0] + dir[0], coord[1] + dir[1]) for dir in DIRS.values()}


def part2(input):
  black_tiles = set()
  for dirs in input:
    coord = (0, 0)
    for dir in dirs:
      coord = (coord[0] + DIRS[dir][0], coord[1] + DIRS[dir][1])
    black_tiles ^= {coord}
  for day in range(1, 101):
    to_flip = set()
    white_neighbors = set()
    for coord in black_tiles:
      all_neighbors = neighbors(coord)
      black_neighbors = black_tiles & all_neighbors
      white_neighbors |= all_neighbors - black_neighbors
      if len(black_neighbors) == 0 or len(black_neighbors) > 2:
        to_flip.add(coord)
    for coord in white_neighbors:
      if len(black_tiles & neighbors(coord)) == 2:
        to_flip.add(coord)
    black_tiles ^= to_flip
    ## if day <= 10 or day % 10 == 0:
      ## print(day, len(black_tiles))
  return len(black_tiles)


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
