from collections import defaultdict
import itertools
import math
from hashlib import md5
import msvcrt
import numpy as np
import os.path
import re
import sys

from intcode import Intcode


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip()

  return [list(map(int, re.search(r'^<x=(-?\d+), y=(-?\d+), z=(-?\d+)>$', line).groups()))
          for line in input.split('\n')]


def do_step(positions, velocities):
  velocities += np.sum(np.sign(positions - positions[:, np.newaxis]), axis=1)
  positions += velocities


def part1(input):
  positions = np.array(input)
  velocities = np.zeros_like(positions)
  for step in range(1000):
    do_step(positions, velocities)
  return np.sum(np.sum(np.abs(positions), axis=1) * np.sum(np.abs(velocities), axis=1))


def part2(input):
  axes = np.array(input).T
  max_offset = 0
  cycles = []
  for axis, positions in enumerate(axes):
    velocities = np.zeros_like(positions)
    initial_state = tuple(np.concatenate((positions, velocities)))
    step = 1
    do_step(positions, velocities)
    while tuple(np.concatenate((positions, velocities))) != initial_state:
      do_step(positions, velocities)
      step += 1
    print('{} cycles in {} steps'.format('XYZ'[axis], step))
    cycles.append(step)
  return np.lcm.reduce(cycles, dtype='i8')


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
