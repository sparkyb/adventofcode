import collections
from collections import defaultdict
import enum
import functools
import itertools
import math
import msvcrt
import os.path
import pdb
import re
import sys

#import numpy as np

from intcode import Intcode


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  return list(map(int, input.split(',')))


def springscript(input, script):
  prog = Intcode(input)
  if not isinstance(script, str):
    script = '\n'.join(line.strip() for line in script if line.strip())
  script = script.strip() + '\n'
  prog.input.extend(map(ord, script))
  prog.run()
  if prog.output[-1] >= 256:
    ret = prog.output.pop()
  else:
    ret = None
  print(''.join(map(chr, prog.output)))
  return ret

def part1(input):
  script = [
      'NOT A J',
      'NOT J T',
      'AND B T',
      'AND C T',
      'NOT T J',
      'AND D J',
      'WALK',
  ]
  return springscript(input, script)


def part2(input):
  script = [
      'OR A J',
      'AND B J',
      'AND C J',
      'NOT J J',
      'AND D J',
      'OR E T',
      'OR H T',
      'AND T J',
      'RUN',
  ]
  return springscript(input, script)


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
