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

  return [map(int,re.search(r'^#(?P<i>\d+)\s+@\s+(?P<x>\d+),(?P<y>\d+):\s*(?P<w>\d+)x(?P<h>\d+)\s*$', line).groups()) for line in input.split('\n')]

def overlap(claim1, claim2):
  i1,x1,y1,w1,h1 = claim1
  i2,x2,y2,w2,h2 = claim2
  x = max(x1,x2)
  y = max(y1,y2)
  w = min(x1+w1,x2+w2) - x
  h = min(y1+h1,y2+h2) - y
  return (x,y,w,h)

def part1(claims):
  overlapped = set()
  for i, claim1 in enumerate(claims):
    for claim2 in claims[i+1:]:
      x1,y1,w,h = overlap(claim1,claim2)
      for x in xrange(x1, x1+w):
        for y in xrange(y1, y1+h):
          overlapped.add((x,y))
  return len(overlapped)

  ## claimed_squares = {}
  ## for i,x1,y1,w,h in input:
    ## for x in xrange(x1, x1+w):
      ## for y in xrange(y1,y1+h):
        ## claimed_squares[(x,y)] = claimed_squares.get((x,y),0) + 1
  ## overlaps = 0
  ## for k,v in claimed_squares.items():
    ## if v > 1:
      ## overlaps += 1
  ## return overlaps

def part2(claims):
  nonoverlapping = []
  for i, claim1 in enumerate(claims):
    for j, claim2 in enumerate(claims):
      if i == j: continue
      x1,y1,w,h = overlap(claim1,claim2)
      if w > 0 and h > 0:
        break
    else:
      nonoverlapping.append(claim1[0])
  return nonoverlapping

  ## claimed_squares = {}
  ## claims = set()
  ## for i,x1,y1,w,h in input:
    ## claims.add(i)
    ## for x in xrange(x1, x1+w):
      ## for y in xrange(y1,y1+h):
        ## claimed_squares.setdefault((x,y),set()).add(i)
  ## for k,v in claimed_squares.items():
    ## if len(v) > 1:
      ## claims -= v
  ## return list(claims)


if __name__ == '__main__':
  input = get_input()
  print part1(input)
  print part2(input)
