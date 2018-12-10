import os.path
import re
import math
from collections import defaultdict
import itertools
import md5
import msvcrt


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0]+'.txt'
  with open(filename) as fp:
    input = fp.read().strip()

  return [map(int, re.search(r'^position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>\s*$', line).groups()) for line in input.split('\n')]


def step(point):
  x, y, dx, dy = point
  x += dx
  y += dy
  return x,y,dx,dy

def draw(points):
  ox = min(x for x,y,dx,dy in points)
  oy = min(y for x,y,dx,dy in points)
  w = max(x for x,y,dx,dy in points)-ox+1
  h = max(y for x,y,dx,dy in points)-oy+1
  if (h > 10): return False
  grid = ['.' * w for y in xrange(h)]
  for x,y,dx,dy in points:
    grid[y-oy] = grid[y-oy][:x-ox] + '#' + grid[y-oy][x-ox+1:]
  print '\n'.join(grid)
  return True

def part1(points):
  i = 0
  while True:
    if (draw(points)):
      if (msvcrt.getch() == chr(27)):
        return i
    points = map(step,points)
    i += 1

def part2(input):
  return None


if __name__ == '__main__':
  input = get_input()
  print part1(input)
  print part2(input)
