from collections import defaultdict
import itertools
import math
from hashlib import md5
import msvcrt
import numpy as np
import os.path
import re
import sys

DIRS = {
  'L': np.array([-1, 0]),
  'R': np.array([1, 0]),
  'U': np.array([0, -1]),
  'D': np.array([0, 1]),
}

def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip()

  return [[DIRS[dir[0]] * int(dir[1:]) for dir in line.split(',')]
          for line in input.split('\n')]

def segments(line):
  ret = []
  p = np.array([0, 0])
  for dist in line:
    p2 = p + dist
    ret.append((p, p2))
    p = np.array(p2)
  return ret

def intersect(seg1, seg2):
  if seg1[0][0] == seg1[1][0] and seg2[0][1] == seg2[1][1]:
    hseg, vseg = seg2, seg1
  elif seg2[0][0] == seg2[1][0] and seg1[0][1] == seg1[1][1]:
    hseg, vseg = seg1, seg2
  else:
    return None
  p = np.array([vseg[0][0], hseg[0][1]])
  l, r = sorted([hseg[0][0], hseg[1][0]])
  t, b = sorted([vseg[0][1], vseg[1][1]])
  if l <= p[0] <= r and t <= p[1] <= b:
    return p
  return None

def part1(input):
  segs = list(map(segments, input))
  dist = None
  for seg1 in segs[0]:
    for seg2 in segs[1]:
      p = intersect(seg1, seg2)
      if p is not None and not np.array_equal(p, (0, 0)):
        d = abs(p).sum()
        if dist is None or d < dist:
          dist = d
  return dist

def part2(input):
  segs = list(map(segments, input))
  dist = None
  d1 = 0
  for seg1 in segs[0]:
    d2 = 0
    for seg2 in segs[1]:
      p = intersect(seg1, seg2)
      if p is not None and not np.array_equal(p, (0, 0)):
        d = d1 + d2 + abs(p - seg1[0]).sum() + abs(p - seg2[0]).sum()
        if dist is None or d < dist:
          dist = d
      d2 += abs(seg2[1] - seg2[0]).sum()
    d1 += abs(seg1[1] - seg1[0]).sum()
  return dist

if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
