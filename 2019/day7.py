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

  return list(map(int, input.split(',')))
  #return input.split('\n')


def part1(input):
  max_thrust = 0
  for phases in itertools.permutations((0,1,2,3,4)):
    signal = 0
    for phase in phases:
      amp = Intcode(input, [phase, signal])
      amp.run()
      signal = amp.output[-1]
    max_thrust = max(max_thrust, signal)
  return max_thrust


def part2(input):
  max_thrust = 0
  for phases in itertools.permutations((5,6,7,8,9)):
    amps = [Intcode(input, [phase]) for phase in phases]
    amps[0].input.append(0)
    while not amps[-1].halted:
      for i, amp in enumerate(amps):
        output = amp.run(return_output=True)
        if output is not None:
          amps[(i + 1) % len(amps)].input.append(output)
    max_thrust = max(max_thrust, amps[-1].output[-1])
  return max_thrust


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
