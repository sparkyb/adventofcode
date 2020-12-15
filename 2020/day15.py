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

  return list(map(int, input.split(',')))


def game(input, target_index):
  prev_index = 0
  prev_num = input[0]
  prev_indexes = {}
  for next_index, next_num in enumerate(input[1:], start=1):
    if prev_num is not None:
      prev_indexes[prev_num] = prev_index
    prev_index = next_index
    prev_num = next_num
  for next_index in range(len(input), target_index):
    if prev_num in prev_indexes:
      age = prev_index - prev_indexes[prev_num]
    else:
      age = 0
    prev_indexes[prev_num] = prev_index
    prev_index = next_index
    prev_num = age
  return prev_num


def part1(input):
  return game(input, 2020)


def part2(input):
  return game(input, 30000000)


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
