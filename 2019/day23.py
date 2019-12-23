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

#import numpy as np

from intcode import Intcode, NeedsInput


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  return list(map(int, input.split(',')))


def part1(input):
  computers = [Intcode(input, [i]) for i in range(50)]
  while True:
    for comp in computers:
      try:
        dest = comp.run(True)
      except NeedsInput:
        comp.input.append(-1)
      else:
        x = comp.run(True)
        y = comp.run(True)
        ## print(dest, x, y)
        if dest == 255:
          return y
        computers[dest].input.extend([x, y])


def part2(input):
  computers = [Intcode(input, [i]) for i in range(50)]
  empty = [0] * len(computers)
  nat = None
  prev_y = None
  while True:
    for i, comp in enumerate(computers):
      try:
        dest = comp.run(True)
      except NeedsInput:
        empty[i] += 1
        if all(e >= 2 for e in empty):
          y = nat[1]
          if y == prev_y:
            return y
          prev_y = y
          computers[0].input.extend(nat)
          empty[0] = 0
        comp.input.append(-1)
      else:
        x = comp.run(True)
        y = comp.run(True)
        ## print(dest, x, y)
        if dest == 255:
          nat = [x, y]
        else:
          computers[dest].input.extend([x, y])
          empty[dest] = 0


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
