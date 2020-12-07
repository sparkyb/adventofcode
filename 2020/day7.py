import collections
from collections import defaultdict
import enum
import functools
import itertools
import math
import msvcrt
import os.path
import re
import sys

#import numpy as np


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  rules = {}
  for line in input.split('\n'):
    match = re.search(
        '^(.*?) bags contain '
        '(no other bags|\d+ .*? bags?(?:, \d+ .*? bags?)*)\.$',
        line)
    key = match.group(1)
    assert key not in rules
    if match.group(2) == 'no other bags':
      rules[key] = []
    else:
      rules[key] = [(int(amount), color)
                    for value in match.group(2).split(', ')
                    for amount, color in
                    [re.search(r'^(\d+) (.*?) bags?$', value).groups()]]
  return rules


def part1(input):
  reversed = defaultdict(set)
  for key, values in input.items():
    for amount, color in values:
      reversed[color].add(key)
  options = set()
  frontier = set(reversed['shiny gold'])
  while frontier:
    option = frontier.pop()
    options.add(option)
    frontier.update(reversed[option])
  return len(options)


def part2(input):
  def num_bags(key):
    return sum(amount * num_bags(color) for amount, color in input[key]) + 1
  return num_bags('shiny gold') - 1


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
