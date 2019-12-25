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

from intcode import Intcode, NeedsInput


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  return list(map(int, input.split(',')))


PATH = [
  'east',
  'take klein bottle',
  'east',
  'take semiconductor',
  'west',
  'north',
  'north',
  #'take infinite loop',
  'north',
  'take dehydrated water',
  'south',
  'south',
  'south',
  'west',
  'north',
  'take sand',
  'north',
  #'take escape pod',
  'north',
  'take astrolabe',
  'south',
  'south',
  'west',
  'west',
  'take mutex',
  'east',
  'east',
  'south',
  'west',
  'north',
  'take shell',
  'south',
  'south',
  #'take giant electromagnet',
  'east',
  #'take photons',
  'south',
  #'take molten lava',
  'north',
  'west',
  'west',
  'take ornament',
  'west',
  'south',
  'drop klein bottle',
  'drop mutex',
  'drop semiconductor',
  'drop dehydrated water',
  'south',
]

def part1(code):
  prog = Intcode(code)
  while True:
    try:
      while True:
        ch = prog.run(True)
        if ch is None:
          break
        print(chr(ch), end='')
    except NeedsInput:
      text = ''.join(map(chr, prog.output))
      ## print(text, end='')
      prog.output = []
      if PATH:
        line = PATH.pop(0)
      else:
        line = input()
      prog.input.extend(list(map(ord, line + '\n')))
  return None


def part2(input):
  return None


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  code = get_input(args.input)
  print(part1(code))
  print(part2(code))
