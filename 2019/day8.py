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


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip()

  return np.array(list(map(int, input))).reshape((-1, 6, 25))


def part1(input):
  min_layer = input[np.argmin(np.sum(input == 0, (1, 2)))]
  return np.sum(min_layer == 1) * np.sum(min_layer == 2)


def part2(input):
  final = np.select(input != 2, input)
  for row in final:
    print(''.join('X' if pixel else ' ' for pixel in row))


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
