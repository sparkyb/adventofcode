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


##   0:      1:      2:      3:      4:
##  aaaa    ....    aaaa    aaaa    ....
## b    c  .    c  .    c  .    c  b    c
## b    c  .    c  .    c  .    c  b    c
##  ....    ....    dddd    dddd    dddd
## e    f  .    f  e    .  .    f  .    f
## e    f  .    f  e    .  .    f  .    f
##  gggg    ....    gggg    gggg    ....
## 
##   5:      6:      7:      8:      9:
##  aaaa    aaaa    aaaa    aaaa    aaaa
## b    .  b    .  .    c  b    c  b    c
## b    .  b    .  .    c  b    c  b    c
##  dddd    dddd    ....    dddd    dddd
## .    f  e    f  .    f  e    f  .    f
## .    f  e    f  .    f  e    f  .    f
##  gggg    gggg    ....    gggg    gggg


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  return [(list(map(set, signals.split())),
           list(map(set, outputs.split())))
          for line in input.split('\n')
          for signals, outputs in [line.split(' | ')]]


def part1(input):
  return sum(len(wires) in (2, 3, 4, 7)
             for _, outputs in input for wires in outputs)


def get_digits(signals):
  digits = [None] * 10
  by_size = collections.defaultdict(list)
  for wires in signals:
    by_size[len(wires)].append(wires)

  digits[1] = by_size[2][0]
  digits[7] = by_size[3][0]
  digits[4] = by_size[4][0]
  digits[8] = by_size[7][0]

  for wires in by_size[6]:
    if not digits[1].issubset(wires):
      digits[6] = wires
    elif digits[4].issubset(wires):
      digits[9] = wires
    else:
      digits[0] = wires

  for wires in by_size[5]:
    if digits[1].issubset(wires):
      digits[3] = wires
    elif wires.issubset(digits[9]):
      digits[5] = wires
    else:
      digits[2] = wires

  return digits


def decode_outputs(digits, outputs):
  return sum(digits.index(wires) * pow(10, i)
             for i, wires in enumerate(reversed(outputs)))


def part2(input):
  return sum(decode_outputs(get_digits(signals), outputs)
             for signals, outputs in input)


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
