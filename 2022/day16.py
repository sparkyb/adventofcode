#!/usr/bin/env python

import collections
from collections import defaultdict
import enum
import functools
import heapq
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

  rates = {}
  tunnels = {}
  for line in input.split('\n'):
    valve, rate, to_valves = re.search(
        r'^Valve ([A-Z]{2}) has flow rate=(\d+); '
        r'tunnels? leads? to valves? ([A-Z]{2}(?:, [A-Z]{2})*)$', line).groups()
    rates[valve] = int(rate)
    tunnels[valve] = to_valves.split(', ')
  return rates, tunnels


class Cave:
  def __init__(self, rates, tunnels):
    self.rates = rates
    self.tunnels = tunnels
    self.useful_valves = frozenset(valve for valve, rate in self.rates.items()
                                   if rate)
    self.times = {}

    frontier = collections.deque()
    for from_valve in self.tunnels:
      self.times[from_valve] = {from_valve: 1}
      frontier.append((from_valve,))
    while frontier:
      path = frontier.popleft()
      from_valve = path[0]
      for to_valve in self.tunnels[path[-1]]:
        if to_valve in path:
          continue
        if (to_valve not in self.times[from_valve] or
            len(path) + 1 < self.times[from_valve][to_valve]):
          new_path = path + (to_valve,)
          self.times[from_valve][to_valve] = len(new_path)
          frontier.append(new_path)

  def calc_pressures(self, t=30, start='AA'):
    pressures = {}

    frontier = collections.deque([(t, start, 0, frozenset())])
    while frontier:
      t, from_valve, pressure, open_valves = frontier.popleft()
      pressures[open_valves] = max(pressures.get(open_valves, 0), pressure)
      for to_valve in self.useful_valves - open_valves:
        new_t = t - self.times[from_valve][to_valve]
        if new_t <= 0:
          continue
        new_pressure = pressure + self.rates[to_valve] * new_t
        new_valves = open_valves | {to_valve}
        frontier.append((new_t, to_valve, new_pressure, new_valves))
    return pressures


def part1(input):
  cave = Cave(*input)
  return max(cave.calc_pressures(30).values())


def part2(input):
  cave = Cave(*input)
  pressures = cave.calc_pressures(26)
  return max(pressures[my_valves] + pressures[elephant_valves]
             for my_valves, elephant_valves in itertools.combinations(pressures, 2)
             if not (my_valves & elephant_valves))


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
