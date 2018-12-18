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

def step(map):
  new_map = []
  for y, row in enumerate(map):
    new_row = ''
    for x, cell in enumerate(row):
      counts = defaultdict(int)
      for y2 in xrange(max(y-1,0),min(y+2,len(map))):
        for x2 in xrange(max(x-1,0),min(x+2,len(map[y2]))):
          if y2 == y and x2 == x:
            continue
          counts[map[y2][x2]] += 1
      if cell == '.' and counts['|'] >= 3:
        cell = '|'
      elif cell == '|' and counts['#'] >= 3:
        cell = '#'
      elif cell == '#' and (counts['#'] < 1 or counts['|'] < 1):
        cell = '.'
      new_row += cell
    new_map.append(new_row)
  return new_map

def steps(map, n):
  steps = ['\n'.join(map)]
  ## print '\n'.join(map)
  for i in xrange(n):
    map = step(map)
    ## print 'After %d minutes:' % (i+1)
    ## print '\n'.join(map)
    ## if msvcrt.getch() == ord(27):
      ## sys.exit()
    flat = '\n'.join(map)
    if flat in steps:
      a = steps.index(flat)
      b = len(steps) - a
      map = steps[(n - a) % b + a].split('\n')
      break
    else:
      steps.append(flat)
  return map

def value(map):
  counts = defaultdict(int)
  for row in map:
    for cell in row:
      counts[cell] += 1
  ## print counts
  return counts['|'] * counts['#']

def part1(map):
  return value(steps(map, 10))

def part2(map):
  return value(steps(map, 1000000000))


if __name__ == '__main__':
  input = get_input()
  print part1(input)
  print part2(input)
