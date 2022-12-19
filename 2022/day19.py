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

  ret = []
  for line in input.split('\n'):
    (ore_ore,
     clay_ore,
     obsidian_ore, obsidian_clay,
     geode_ore, geode_obsidian) = map(
        int,
        re.search(
            r'^Blueprint (?:\d+): Each ore robot costs (\d+) ore\. '
            r'Each clay robot costs (\d+) ore\. '
            r'Each obsidian robot costs (\d+) ore and (\d+) clay\. '
            r'Each geode robot costs (\d+) ore and (\d+) obsidian\.$',
            line).groups())
    ret.append(((ore_ore, 0, 0, 0),
                (clay_ore, 0, 0, 0),
                (obsidian_ore, obsidian_clay, 0, 0),
                (geode_ore, 0, geode_obsidian, 0)))
  return ret


def max_geodes(costs, t=24):
  robots = (1, 0, 0, 0)
  resources = (0, 0, 0, 0)
  visited = set()
  frontier = collections.deque([(t, robots, resources)])
  best = 0
  while frontier:
    t, robots, resources = frontier.popleft()
    # don't hold more than you can spend in the rest of the time
    resources = tuple(min(r, max(cost[i] for cost in costs) * t)
                      for i, r in enumerate(resources[:-1])) + resources[-1:]
    # don't make more in a minute than you can spend in a minute
    robots = tuple(min(b, max(cost[i] for cost in costs))
                   for i, b in enumerate(robots[:-1])) + robots[-1:]
    if (t, robots, resources) in visited:
      continue
    visited.add((t, robots, resources))
    # the number I'll produce if I buy no more bots
    geodes = resources[-1] + robots[-1] * t
    if geodes > best:
      ## print(f'  {geodes}')
      best = geodes
    if t == 0:
      continue
    n = t - 1
    # even if we buy a new geode bot every minute, we still won't do better
    if resources[-1] + robots[-1] * t + (n * (n + 1) // 2) < best:
      continue
    if all(c <= r for c, r in zip(costs[-1], resources)):
      # if we can afford a geode bot, always just do that
      cost = costs[-1]
      new_robots = tuple(r + (i == len(robots) - 1)
                         for i, r in enumerate(robots))
      new_resources = tuple(r - c + b
                            for c, r, b in zip(cost, resources, robots))
      frontier.append((t - 1, new_robots, new_resources))
      continue
    else:
      # otherwise, explore all paths
      for robot_type, cost in enumerate(costs):
        # time until we can afford this thing
        dt = max(0 if c <= r else t if b == 0 else math.ceil((c - r) / b)
                 for c, r, b in zip(cost, resources, robots)) + 1
        if dt < t:
          new_robots = tuple(r + (i == robot_type)
                             for i, r in enumerate(robots))
          new_resources = tuple(r - c + b * dt
                                for c, r, b in zip(cost, resources, robots))
          frontier.append((t - dt, new_robots, new_resources))
  return best


def part1(input):
  score = 0
  for i, costs in enumerate(input, start=1):
    ## print(i)
    m = max_geodes(costs)
    ## print(f'  {m}')
    score += i * m
  return score


def part2(input):
  score = 1
  for i, costs in enumerate(input[:3], start=1):
    ## print(i)
    m = max_geodes(costs, 32)
    ## print(f'  {m}')
    score *= m
  return score


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
