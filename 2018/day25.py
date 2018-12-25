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

  return set(tuple(map(int, line.split(','))) for line in input.split('\n'))


def manhattan_distance(p1, p2):
  return sum(abs(c1-c2) for c1,c2 in zip(p1,p2))


def part1(points):
  connected = {}
  for p1 in points:
    connected[p1] = set()
    for p2 in points:
      if manhattan_distance(p1,p2) <= 3:
        connected[p1].add(p2)

  constellations = []
  while connected:
    constellation = set()
    frontier = set([connected.keys()[0]])
    while frontier:
      point = frontier.pop()
      if point not in connected:
        continue
      constellation.add(point)
      frontier.update(connected.pop(point))
    constellations.append(constellation)
  return len(constellations)

def part2(input):
  return None


if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser(usage='%prog [options] [<input.txt>]')
  options, args = parser.parse_args()
  input = get_input(*args)
  print part1(input)
  print part2(input)
