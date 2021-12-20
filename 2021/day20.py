#!/usr/bin/env python

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

  algo, image = input.split('\n\n')
  algo = [c == '#' for c in algo]
  image = {(y, x) for y, line in enumerate(image.split('\n')) for x, c in enumerate(line) if c == '#'}
  return algo, image


def step(algo, input, input_inverted=False):
  output = set()
  output_inverted = algo[-1 if input_inverted else 0]
  min_x = min(x for _, x in input)
  max_x = max(x for _, x in input)
  min_y = min(y for y, _ in input)
  max_y = max(y for y, _ in input)
  for y in range(min_y - 1, max_y + 2):
    for x in range(min_x - 1, max_x + 2):
      i = 0
      for y2 in range(y - 1, y + 2):
        for x2 in range(x - 1, x + 2):
          i <<= 1
          if ((y2, x2) in input) ^ input_inverted:
            i |= 1
      if algo[i] ^ output_inverted:
        output.add((y, x))
  return output, output_inverted


def part1(input):
  algo, image = input
  inverted = False
  for _ in range(2):
    image, inverted = step(algo, image, inverted)
  assert not inverted
  return len(image)


def part2(input):
  algo, image = input
  inverted = False
  for _ in range(50):
    image, inverted = step(algo, image, inverted)
  assert not inverted
  return len(image)


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('-c', '--clip', '--copy', action='store_true',
                      help='Copy answer to clipboard')
  parser.add_argument('-p', '--part', type=int, choices=(1, 2),
                      help='Which part to run (default: both)')
  parser.add_argument('-1', '--part1', action='store_const', dest='part',
                      const=1, help='Part 1 only')
  parser.add_argument('-2', '--part2', action='store_const', dest='part',
                      const=2, help='Part 2 only')
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  if args.clip:
    import pyperclip
  input = get_input(args.input)
  if not args.part or args.part == 1:
    answer1 = part1(input)
    print(answer1)
    if args.clip and answer1 is not None:
      pyperclip.copy(str(answer1))
  if not args.part or args.part == 2:
    answer2 = part2(input)
    print(answer2)
    if args.clip and answer2 is not None:
      pyperclip.copy(str(answer2))
