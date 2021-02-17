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

  return list(map(int, input.split('\n')))


def transform(subject, loop):
  value = 1
  for _ in range(loop):
    value = (value * subject) % 20201227
  return value


def reverse_transform(subject, public):
  loop = 0
  value = 1
  while value != public:
    value = (value * subject) % 20201227
    loop += 1
  return loop


def part1(input):
  card_public, door_public = input
  card_loop = reverse_transform(7, card_public)
  print('card loop: {}'.format(card_loop))
  door_loop = reverse_transform(7, door_public)
  print('door loop: {}'.format(door_loop))
  key = transform(door_public, card_loop)
  assert key == transform(card_public, door_loop)
  return key


def part2(input):
  return None


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
