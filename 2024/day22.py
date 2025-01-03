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

  return [int(n) for n in input.split('\n')]


def mix(secret, num):
  return secret ^ num


def prune(secret):
  return secret % 16777216


def next_secret(secret):
  secret = prune(mix(secret, secret << 6))
  secret = prune(mix(secret, secret >> 5))
  secret = prune(mix(secret, secret << 11))
  return secret


def part1(input):
  result = 0
  for secret in input:
    for _ in range(2000):
      secret = next_secret(secret)
    result += secret
  return result


def part2(input):
  totals = collections.Counter()
  for secret in input:
    bananas = {}
    changes = collections.deque(maxlen=4)
    price = secret % 10
    for i in range(2000):
      prev_price = price
      secret = next_secret(secret)
      price = secret % 10
      changes.append(price - prev_price)
      if i >= 3:
        key = tuple(changes)
        if key not in bananas:
          bananas[key] = price
    totals.update(bananas)
  return max(totals.values())


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
