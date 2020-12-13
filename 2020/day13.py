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

  t, buses = input.split('\n')
  return int(t), [int(bus) if bus != 'x' else None for bus in buses.split(',')]


def part1(input):
  t, buses = input
  buses = {bus for bus in buses if bus is not None}
  wait, bus = min((-t % bus, bus) for bus in buses)
  return wait * bus


def lcm(*nums):
  return functools.reduce(lambda n, lcm: lcm * n // math.gcd(lcm, n), nums)


def part2(input):
  _, buses = input
  buses = [(offset, bus) for offset, bus in enumerate(buses) if bus is not None]
  start = 0
  step = 1
  found = 0
  while found < len(buses):
    for t in itertools.count(start, step):
      matches = [bus for offset, bus in buses if (t + offset) % bus == 0]
      if len(matches) > found:
        ## print('matched {} @ {}'.format(matches, t))
        start = t
        step = lcm(*matches)
        found = len(matches)
        break
  return start


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
