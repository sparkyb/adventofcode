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

  return list(map(int, input.split(',')))


def part1(input):
  prog = Intcode(input)
  prog.run()
  s = ''.join(map(chr, prog.output)).strip()
  print(s)
  grid = np.array([list(line) for line in s.split('\n')])
  alignment = 0
  for y in range(1, grid.shape[0] - 1):
    for x in range(1, grid.shape[1] - 1):
      if (grid[y, x] != '.' and
          grid[y - 1, x] != '.' and grid[y + 1, x] != '.' and
          grid[y, x - 1] != '.' and grid[y, x + 1] != '.'):
        alignment += x * y
  return alignment


def part2(input):
  code = ['A,B,B,C,A,B,C,A,B,C',
          'L,6,R,12,L,4,L,6',
          'R,6,L,6,R,12',
          'L,6,L,10,L,10,R,6',
          'n']
  code = '\n'.join(code) + '\n'
  prog = Intcode(input)
  prog[0] = 2
  prog.input = list(map(ord, code))
  prog.run()
  assert not prog.input
  return prog.output[-1]


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
