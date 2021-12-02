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

  lines = [line.split() for line in input.split('\n')]
  return [(dir, int(amount)) for dir, amount in lines]



def part1(input):
  x = 0
  y = 0
  for dir, amount in input:
    if dir == 'forward':
      x += amount
    elif dir == 'down':
      y += amount
    elif dir == 'up':
      y -= amount
  return x * y


def part2(input):
  x = 0
  y = 0
  aim = 0
  x = 0
  y = 0
  for dir, amount in input:
    if dir == 'forward':
      x += amount
      y += amount * aim
    elif dir == 'down':
      aim += amount
    elif dir == 'up':
      aim -= amount
  return x * y


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
