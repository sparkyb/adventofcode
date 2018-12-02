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

  return input.split('\n')


def part1(input):
  twos = 0
  threes = 0
  for line in input:
    two = 0
    three = 0
    for c in line:
      count = line.count(c)
      if count == 2:
        two = 1
      elif count == 3:
        three = 1
    twos += two
    threes += three
  return twos * threes

def part2(input):
  for i, line1 in enumerate(input):
    for line2 in input[i+1:]:
      diff = -1
      for j in xrange(len(line1)):
        if line1[j] != line2[j]:
          if diff >= 0:
            break
          else:
            diff = j
      else:
        if diff >= 0:
          return line1[:diff]+line1[diff+1:]
  return None


if __name__ == '__main__':
  input = get_input()
  print part1(input)
  print part2(input)
