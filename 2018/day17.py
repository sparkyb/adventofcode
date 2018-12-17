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

  clay = set()
  for line in input.split('\n'):
    match = re.search(r'^x=(\d+), y=(\d+)\.\.(\d+)$', line)
    if match:
      x, y1, y2 = map(int,match.groups())
      for y in xrange(y1, y2 + 1):
        clay.add((y,x))
    match = re.search(r'^y=(\d+), x=(\d+)\.\.(\d+)$', line)
    if match:
      y, x1, x2 = map(int,match.groups())
      for x in xrange(x1, x2 + 1):
        clay.add((y,x))
  return clay


SPRING = (0,500)


def fill(clay):
  clay = set(clay)
  top = min(y for y,x in clay)
  bottom = max(y for y,x in clay)
  filled = set(clay)
  wet = set()

  down = set([SPRING])
  while down:
    y, x = down.pop()
    orig_y = y
    while y <= bottom:
      if y >= top:
        wet.add((y, x))
      if (y + 1, x) in filled:
        # found bottom, try to fill across
        ## down2 = fill_across(y, x, top, bottom, filled, wet)
        ## if down2:
          ## # overflowed
          ## down.update(down2)
        ## else:
          ## # filled, start again from the top
          ## down.add(SPRING)

        while y >= orig_y:
          down2 = fill_across(y, x, top, bottom, filled, wet)
          if down2:
            # overflowed
            down.update(down2)
            break
          else:
            # filled bottom, try filling a row up
            y -= 1
        if y < orig_y:
          # filled all the way up, try again from the top
          down.add(SPRING)

        break
      y += 1
  return filled - clay, wet

def fill_across(y, x, top, bottom, filled, wet):
  down = []
  left = x
  while True:
    if y >= top:
      wet.add((y, left))
    if (y + 1, left) not in filled:
      down.append((y, left))
      break
    elif (y, left - 1) in filled:
      break
    left -= 1
  right = x
  while True:
    if y >= top:
      wet.add((y, right))
    if (y + 1, right) not in filled:
      down.append((y, right))
      break
    elif (y, right + 1) in filled:
      break
    right += 1
  if not down:
    for x in xrange(left, right + 1):
      filled.add((y, x))
  return down

def draw(clay, filled, wet):
  bottom = max(y for y, x in clay)
  left = min(x for y, x in filled|wet|clay)
  right = max(x for y, x in filled|wet|clay)
  map = ''
  for y in xrange(0, bottom + 1):
    for x in xrange(left, right + 1):
      if (y, x) == SPRING:
        map += '+'
      elif (y, x) in clay:
        map += '#'
      elif (y, x) in filled:
        map += '~'
      elif (y, x) in wet:
        map += '|'
      else:
        map += '.'
    map += '\n'
  return map

def part1(clay):
  filled, wet = fill(clay)
  return len(wet)

def part2(clay):
  filled, wet = fill(clay)
  return len(filled)


if __name__ == '__main__':
  input = get_input()
  print part1(input)
  print part2(input)
