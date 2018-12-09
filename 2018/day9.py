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

  return map(int, re.search(r'^(\d+) players; last marble is worth (\d+) points$', input).groups())


def part1(input):
  players, marbles = input
  scores = [0] * players
  player = 0
  marble = 1
  current = {'value': 0}
  current['next'] = current
  current['prev'] = current
  while marble <= marbles:
    if marble % 23 == 0:
      for i in xrange(7):
        current = current['prev']
      scores[player] += marble + current['value']
      current = current['next']
      current['prev'] = current['prev']['prev']
      current['prev']['next'] = current
    else:
      current = current['next']
      current = {'value': marble, 'next': current['next'], 'prev': current}
      current['prev']['next'] = current
      current['next']['prev'] = current
    marble += 1
    player = (player + 1) % len(scores)
  return max(scores)

def part2(input):
  players, marbles = input
  return part1((players, marbles*100))


if __name__ == '__main__':
  input = get_input()
  print part1(input)
  print part2(input)
