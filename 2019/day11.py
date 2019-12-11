from collections import defaultdict
import itertools
import math
from hashlib import md5
import msvcrt
import numpy as np
import os.path
import re
import sys

from intcode import Intcode


TURN = [
    np.array([[0, 1], [-1, 0]]),
    np.array([[0, -1], [1, 0]]),
]


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip()

  return list(map(int, input.split(',')))


def paint(input, start_color=0):
  coord = np.array((0, 0))
  dir = np.array((-1, 0))
  ship = defaultdict(int)
  ship[tuple(coord)] = start_color
  prog = Intcode(input, [])
  while True:
    prog.input.append(ship[tuple(coord)])
    color = prog.run(True)
    if color is None:
      break
    ship[tuple(coord)] = color
    turn = TURN[prog.run(True)]
    dir = dir.dot(turn)
    coord += dir
  return ship


def part1(input):
  ship = paint(input)
  return len(ship)


def part2(input):
  ship = paint(input, 1)
  whites = np.array([coord for coord, color in ship.items() if color])
  origin = np.min(whites, axis=0)
  whites -= origin
  grid = np.full(np.max(whites, axis=0) + 1, ' ')
  grid[tuple(whites.T)] = '#'
  for row in grid:
    print(''.join(row))


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
