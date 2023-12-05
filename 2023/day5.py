#!/usr/bin/env python

import bisect
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

  sections = input.split('\n\n')
  seeds = [int(n) for n in sections[0].split(':')[1].strip().split()]
  maps = []
  for section in sections[1:]:
    lines = section.split('\n')
    maps.append([])
    for line in lines[1:]:
      dest, src, count = [int(n) for n in line.split()]
      maps[-1].append((src, count, dest))
    maps[-1].sort()
  return seeds, maps


def map_ranges(ranges, src_ranges):
  dest_ranges = []
  srcs = [src for src, _, _ in ranges]
  for src_start, src_count in src_ranges:
    index = bisect.bisect(srcs, src_start) - 1
    while src_count:
      if index >= 0:
        src, count, dest = ranges[index]
        if src_start < src + count:
          dest_count = min(src_count, src + count - src_start)
          dest_ranges.append((src_start + dest - src, dest_count))
          src_start += dest_count
          src_count -= dest_count
      if src_count:
        if index + 1 < len(ranges):
          dest_count = min(src_count, ranges[index + 1][0] - src_start)
        else:
          dest_count = src_count
        if dest_count:
          dest_ranges.append((src_start, dest_count))
        src_start += dest_count
        src_count -= dest_count
      index += 1
  return dest_ranges


def seeds_to_locations(maps, seeds):
  values = seeds
  for ranges in maps:
    values = map_ranges(ranges, values)
  return values


def part1(input):
  seeds, maps = input
  seeds = [(seed, 1) for seed in seeds]
  locations = seeds_to_locations(maps, seeds)
  return min(location for location, _ in locations)


def part2(input):
  seeds, maps = input
  seeds = list(zip(seeds[0::2], seeds[1::2]))
  locations = seeds_to_locations(maps, seeds)
  return min(location for location, _ in locations)


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
