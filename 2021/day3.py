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

  return input.split('\n')


def part1(input):
  gamma = 0
  epsilon = 0
  for bits in zip(*input):
    gamma <<= 1
    epsilon <<= 1
    count = sum(int(bit) * 2 - 1 for bit in bits)
    if count > 0:
      gamma |= 1
    else:
      epsilon |= 1
  return gamma * epsilon


def part2(input):
  def filter(numbers, highest):
    numbers = set(numbers)
    i = 0
    while len(numbers) > 1:
      count = sum((number[i] == '1') * 2 - 1 for number in numbers)
      numbers = set(number for number in numbers
                    if number[i] == '01'[count >= 0 if highest else count < 0])
      i += 1
    assert len(numbers) == 1
    return int(list(numbers)[0], 2)

  o2 = filter(input, True)
  co2 = filter(input, False)
  return o2 * co2


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
