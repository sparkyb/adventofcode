from collections import defaultdict
import itertools
import math
from hashlib import md5
import msvcrt
import numpy as np
import os.path
import re
import sys


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip()

  return list(map(int, input.split('\n')))


def fuel(mass):
  return max((mass // 3) - 2, 0)

def part1(input):
  return sum(fuel(mass) for mass in input)

def part2(input):
  f_total = 0
  for mass in input:
    f = fuel(mass)
    while f:
      f_total += f
      f = fuel(f)
  return f_total


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
