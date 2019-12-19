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

#import numpy as np

from intcode import Intcode


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip()

  return list(map(int, input.split(',')))


def test_coord(prog, x, y):
  prog.reset()
  prog.input.append(x)
  prog.input.append(y)
  return prog.run(True)


def part1(input):
  prog = Intcode(input)
  pulled = 0
  for y in range(50):
    row = ''
    for x in range(50):
      if test_coord(prog, x, y):
        row += '#'
        pulled += 1
      else:
        row += '.'
    print(row)
  return pulled


def part2(input):
  prog = Intcode(input)
  y = 1
  x0 = 0
  x1 = 0
  # find first line with any tractor beam (not counting the required (0,0))
  while not x1:
    for x in range(50):
      if test_coord(prog, x, y):
        x0 = x
        x1 = x + 1
        break
    else:
      y += 1
  # for each line,
  while True:
    # find the left edge of the beam
    while not test_coord(prog, x0, y):
      x0 += 1
      x1 += 1
    # find the right edge of the beam
    while test_coord(prog, x1, y):
      x1 += 1
    # if the beam is wide enough at the top, test the bottom left
    if x1 - x0 >= 100 and test_coord(prog, x1 - 100, y + 99):
        # scan to see if we can move the square any farther left
        for x in range(x1 - 101, x0, -1):
          if not test_coord(prog, x, y + 99):
            return (x + 1) * 10000 + y
        else:
          return x0 * 10000 + y
    ## print('{}: {}-{} = {}'.format(y, x0, x1, x1 - x0))
    y += 1


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
