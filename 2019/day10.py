from collections import defaultdict
import itertools
import math
from hashlib import md5
import msvcrt
#import numpy as np
import os.path
import re
import sys

from intcode import Intcode


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip()

  return [(x, y) for y, line in enumerate(input.split('\n'))
          for x, c in enumerate(line) if c == '#']


def visible_asteroids(source, asteroids):
  """Groups asteroids by angle from the source and sorted by distance.

  Args:
    source: An (x, y) tuple of the asteroid to measure from.
    asteroids: A list of (x, y) locations of asteroids.
  Returns:
    A dictionary mapping (dx, dy) direction vectors to a sorted list of target
    asteroid (x, y) locations in that direction (near to far).
  """
  targets = defaultdict(list)
  for target in asteroids:
    if source == target:
      continue
    dx = target[0] - source[0]
    dy = target[1] - source[1]
    dist = math.gcd(abs(dx), abs(dy))
    dx /= dist
    dy /= dist
    targets[(dx, dy)].append((dist, target))
  for direction in targets:
    targets[direction] = [target for dist, target in sorted(targets[direction])]
  return targets


def best_asteroid(asteroids):
  """Finds best source asteroid that can see the most other asteroids.

  Args:
    asteroids: A list of (x, y) locations of asteroids.
  Returns:
    A dictionary mapping (dx, dy) direction vectors to a sorted list of target
    asteroid (x, y) locations in that direction (near to far). The dictionary
    of targets returned will be the one for the source that maximizes the
    number of keys in the dictionary (i.e. the number of asteroids that can be
    seen).
  """
  best_targets = {}
  for source in asteroids:
    targets = visible_asteroids(source, asteroids)
    if len(targets) > len(best_targets):
      best_targets = targets
  return best_targets


def dir_to_angle(direction):
  """Converts a direction vector into an angle.

  Args:
    direction: A (dx, dy) direction vector.
  Returns:
    An angle in degrees clockwise from up (0-360).
  """
  dx, dy = direction
  return (math.degrees(math.atan2(dy, dx)) + 90) % 360


def sorted_targets(targets):
  """Sorts targets by the order they'd be hit.

  Args:
    targets: A dictionary mapping (dx, dy) direction vectors to a sorted list
    of target asteroid (x, y) locations in that direction (near to far).
  Yields:
    Target (x, y) locations in the order they'd be hit.
  """
  directions = list(targets.keys())
  directions.sort(key=dir_to_angle)
  targets = [targets[direction] for direction in directions]
  return filter(None,
                itertools.chain.from_iterable(itertools.zip_longest(*targets)))


def part1(input):
  return len(best_asteroid(input))


def part2(input):
  targets = best_asteroid(input)
  target = next(itertools.islice(sorted_targets(targets), 199, None))
  return target[0] * 100 + target[1]


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
