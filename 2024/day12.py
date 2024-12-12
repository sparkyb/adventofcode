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

  return {(y, x): c for y, row in enumerate(input.split('\n'))
          for x, c in enumerate(row)}


def traverse_region(input, start):
  plant = input[start]
  region = set()
  frontier = {start}
  while frontier:
    pos = frontier.pop()
    region.add(pos)
    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
      neighbor = (pos[0] + dy, pos[1] + dx)
      if neighbor not in region and neighbor not in frontier and input.get(neighbor) == plant:
        frontier.add(neighbor)
  return region


def calc_perimeter(region):
  return sum(1 for y, x in region
             for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1))
             if (y + dy, x + dx) not in region)


def traverse_side(region, y, x, dy, dx):
  side = set()
  if dy:
    dx = 0
    while (y, x + dx) in region and (y + dy, x + dx) not in region:
      side.add((y, x + dx, dy, 0))
      dx -= 1
    dx = 1
    while (y, x + dx) in region and (y + dy, x + dx) not in region:
      side.add((y, x + dx, dy, 0))
      dx += 1
  else:
    dy = 0
    while (y + dy, x) in region and (y + dy, x + dx) not in region:
      side.add((y + dy, x, 0, dx))
      dy -= 1
    dy = 1
    while (y + dy, x) in region and (y + dy, x + dx) not in region:
      side.add((y + dy, x, 0, dx))
      dy += 1
  return side


def calc_sides(region):
  edges = set()
  for y, x in region:
    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
      if (y + dy, x + dx) not in region:
        edges.add((y, x, dy, dx))
  visited = set()
  sides = 0
  for edge in edges:
    if edge in visited:
      continue
    visited.update(traverse_side(region, *edge))
    sides += 1
  return sides


def part1(input):
  visited = set()
  regions = []
  for pos in input:
    if pos in visited:
      continue
    region = traverse_region(input, pos)
    visited.update(region)
    regions.append(region)
  return sum(len(region) * calc_perimeter(region) for region in regions)


def part2(input):
  visited = set()
  regions = []
  for pos in input:
    if pos in visited:
      continue
    region = traverse_region(input, pos)
    visited.update(region)
    regions.append(region)
  return sum(len(region) * calc_sides(region) for region in regions)


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
