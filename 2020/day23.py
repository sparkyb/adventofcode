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

  return list(map(int, input))


def make_linked_list(order, highest=None):
  if highest is None:
    highest = max(order)
  cups = [i + 1 for i in range(highest)] + [1]
  if highest > max(order):
    prev_cup = highest
    next_cup = max(order) + 1
  else:
    prev_cup = order[-1]
    next_cup = order[0]
  for cup in order:
    cups[prev_cup] = cup
    prev_cup = cup
  cups[prev_cup] = next_cup
  return cups, order[0]


def move(cups, head):
  removed = [cups[head]]
  while len(removed) < 3:
    removed.append(cups[removed[-1]])
  cups[head] = cups[removed[-1]]
  after = head - 1
  while after < 1 or after in removed:
    after -= 1
    if after < 1:
      after = len(cups) - 1
  cups[removed[-1]] = cups[after]
  cups[after] = removed[0]
  return cups[head]


def part1(input):
  cups, head = make_linked_list(input)
  for i in range(100):
    head = move(cups, head)
  result = []
  cup = cups[1]
  while cup != 1:
    result.append(cup)
    cup = cups[cup]
  return ''.join(map(str, result))


def part2(input):
  cups, head = make_linked_list(input, highest=1_000_000)
  for i in range(10_000_000):
    head = move(cups, head)
  return cups[1] * cups[cups[1]]


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
