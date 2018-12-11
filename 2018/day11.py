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

  return int(input)


def power(x, y, input):
  rack = x + 10
  p = rack * y
  p += input
  p *= rack
  p = (p / 100) % 10
  p -= 5
  return p


def part1(input):
  grid = [[power(x,y,input) for x in xrange(1,301)] for y in xrange(1,301)]
  maxpower = None
  maxcoord = None
  for y1 in xrange(1, 299):
    for x1 in xrange(1, 299):
      p = sum(grid[y][x] for x in xrange(x1-1, x1+2) for y in xrange(y1-1, y1+2))
      if maxcoord is None or p > maxpower:
        maxpower = p
        maxcoord = (x1,y1)
  return ','.join(map(str,maxcoord))

def part2(input):
  grid = [[power(x,y,input) for x in xrange(1,301)] for y in xrange(1,301)]
  maxpower = None
  maxcoord = None
  for s in xrange(1, 301):
    ## print s
    rows = [sum(grid[y][x] for x in xrange(s-1)) for y in xrange(300)]
    for x1 in xrange(1, 301-s+1):
      for y in xrange(300):
        rows[y] += grid[y][x1+s-2]
      p = sum(rows[y] for y in xrange(s-1))
      for y1 in xrange(1, 301-s+1):
        p += rows[y1 + s - 2]
        if maxcoord is None or p > maxpower:
          maxpower = p
          maxcoord = (x1,y1,s)
          ## print ','.join(map(str,maxcoord))
        p -= rows[y1-1]
      for y in xrange(300):
        rows[y] -= grid[y][x1-1]
  return ','.join(map(str,maxcoord))

if __name__ == '__main__':
  input = get_input()
  print part1(input)
  print part2(input)
