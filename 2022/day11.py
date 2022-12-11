#!/usr/bin/env python

import collections
from collections import defaultdict
import copy
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

  monkeys = []
  for section in input.split('\n\n'):
    monkey = {}
    lines = section.split('\n')
    match = re.search(r'^  Starting items: (\d+(?:, \d+)*)$', lines[1])
    monkey['items'] = collections.deque(map(int, match.group(1).split(', ')))
    match = re.search(r'^  Operation: new = old ([+*]) (\d+|old)$', lines[2])
    monkey['op'] = match.group(1)
    monkey['op_num'] = match.group(2)
    if monkey['op_num'].isdigit():
      monkey['op_num'] = int(monkey['op_num'])
    match = re.search(r'^  Test: divisible by (\d+)$', lines[3])
    monkey['test'] = int(match.group(1))
    match = re.search(r'^    If true: throw to monkey (\d+)$', lines[4])
    if_true = int(match.group(1))
    match = re.search(r'^    If false: throw to monkey (\d+)$', lines[5])
    if_false = int(match.group(1))
    monkey['next'] = [if_false, if_true]
    monkeys.append(monkey)

  return monkeys


def do_round(monkeys, mod=None):
  for monkey in monkeys:
    while monkey['items']:
      monkey['inspections'] = monkey.get('inspections', 0) + 1
      worry = monkey['items'].popleft()
      op_num = monkey['op_num']
      if op_num == 'old':
        op_num = worry
      if monkey['op'] == '+':
        worry += op_num
      elif monkey['op'] == '*':
        worry *= op_num
      if mod:
        worry %= mod
      else:
        worry //= 3
      next = monkey['next'][worry % monkey['test'] == 0]
      monkeys[next]['items'].append(worry)


def part1(input):
  monkeys = copy.deepcopy(input)
  for round in range(20):
    do_round(monkeys)
  inspections = sorted((monkey['inspections'] for monkey in monkeys),
                       reverse=True)
  return inspections[0] * inspections[1]


def part2(input):
  monkeys = copy.deepcopy(input)
  mod = math.prod(monkey['test'] for monkey in monkeys)
  for round in range(10000):
    do_round(monkeys, mod)
  inspections = sorted((monkey['inspections'] for monkey in monkeys),
                       reverse=True)
  return inspections[0] * inspections[1]


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
