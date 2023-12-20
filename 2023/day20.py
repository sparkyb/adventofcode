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

  modules = {}
  for line in input.split('\n'):
    match = re.search(
        r'^(?:([&%])([a-z]{2})|(broadcaster)) -> ((?:[a-z]{2}, )*[a-z]{2})$',
        line)
    modules[match.group(2) or match.group(3)] = {
        'type': match.group(1),
        'dest': match.group(4).split(', '),
    }
  return modules


def part1(input):
  state = {}
  for key, module in input.items():
    if module['type'] == '%':
      state[key] = False
    for dest in module['dest']:
      if dest in input and input[dest]['type'] == '&':
        state.setdefault(dest, {})[key] = False
  pulses = [0, 0]
  for _ in range(1000):
    queue = [('button', False, 'broadcaster')]
    while queue:
      src, pulse, key = queue.pop(0)
      pulses[pulse] += 1
      if key not in input:
        continue
      module = input[key]
      if module['type'] == '%':
        if not pulse:
          state[key] = not state[key]
          for dest in module['dest']:
            queue.append((key, state[key], dest))
      elif module['type'] == '&':
        state[key][src] = pulse
        new_pulse = not all(state[key].values())
        for dest in module['dest']:
          queue.append((key, new_pulse, dest))
      else:
        for dest in module['dest']:
          queue.append((key, pulse, dest))
  return math.prod(pulses)


def part2(input):
  cycles = []
  for key in input['broadcaster']['dest']:
    value = 0
    bit = 0
    while key:
      next_key = None
      for dest in input[key]['dest']:
        if input[dest]['type'] == '&':
          assert ((value >> bit) & 1) == 0
          value |= 1 << bit
        else:
          assert input[dest]['type'] == '%'
          assert next_key is None
          next_key = dest
      key = next_key
      bit += 1
    cycles.append(value)
  return math.lcm(*cycles)


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
