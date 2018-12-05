import os.path
import re
import math
from collections import defaultdict
import itertools
import md5


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0]+'.txt'
  with open(filename) as fp:
    input = fp.read().strip()

  return input


def react(input):
  changed = True
  while changed:
    changed = False
    i = 0
    while i < len(input) - 1:
      if input[i] != input[i+1] and input[i].lower() == input[i+1].lower():
        input = input[:i]+input[i+2:]
        changed = True
      else:
        i += 1
  return input

def part1(input):
  return len(react(input))

def part2(input):
  input = react(input)
  options = set(input.lower())
  shortest = len(input)
  for option in options:
    l = len(react(input.replace(option,'').replace(option.upper(),'')))
    if l < shortest:
      shortest = l
  return shortest


if __name__ == '__main__':
  input = get_input()
  print part1(input)
  print part2(input)
