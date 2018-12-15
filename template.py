import os.path
import re
import math
from collections import defaultdict
import itertools
import md5
import msvcrt
import sys


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0]+'.txt'
  with open(filename) as fp:
    input = fp.read().rstrip()

  return input.split('\n')


def part1(input):
  return None

def part2(input):
  return None


if __name__ == '__main__':
  input = get_input()
  print part1(input)
  print part2(input)
