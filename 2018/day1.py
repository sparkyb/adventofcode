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

  return map(int,input.split('\n'))


def part1(input):
  return sum(input)

def part2(input):
  freq = 0
  freqs = set([freq])
  i = 0
  while True:
    freq += input[i % len(input)]
    i += 1
    if freq in freqs:
      return freq
    else:
      freqs.add(freq)


if __name__ == '__main__':
  input = get_input()
  print part1(input)
  print part2(input)
