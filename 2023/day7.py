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

  return [(cards, int(bid))
          for cards, bid in (line.split() for line in input.split('\n'))]


CARD_RANK = '23456789TJQKA'
TYPE_RANK = [
    (1, 1, 1, 1, 1),
    (1, 1, 1, 2),
    (1, 2, 2),
    (1, 1, 3),
    (2, 3),
    (1, 4),
    (5,),
]


def hand_rank(cards, jokers=False):
  counts = collections.Counter(cards)
  if jokers:
    num_jokers = counts.pop('J', 0)
  else:
    num_jokers = 0
  counts = sorted(counts.values())
  if counts:
    counts[-1] += num_jokers
  else:
    counts = [num_jokers]
  type_rank = TYPE_RANK.index(tuple(counts))
  card_ranks = tuple(CARD_RANK.index(card) if not jokers or card != 'J' else -1
                     for card in cards)
  return (type_rank,) + card_ranks


def part1(input):
  hands = sorted(input, key=lambda hand: hand_rank(hand[0]))
  return sum(i * bid for i, (cards, bid) in enumerate(hands, start=1))


def part2(input):
  hands = sorted(input, key=lambda hand: hand_rank(hand[0], jokers=True))
  return sum(i * bid for i, (cards, bid) in enumerate(hands, start=1))


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
