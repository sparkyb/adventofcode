import collections
from collections import defaultdict
import enum
import functools
import itertools
import math
import msvcrt
import operator
import os.path
import re
import sys

#import numpy as np


OPS = {
    '+': operator.add,
    '*': operator.mul,
}


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  return [[int(token) if token.isdigit() else token
           for token in re.findall(r'\d+|[(){}]'.format(''.join(OPS.keys())),
                                   line)]
          for line in input.split('\n')]


def eval_math(tokens, i=0, do_last=None):
  results = []
  left = 0
  op = operator.add
  while i < len(tokens):
    if tokens[i] in OPS:
      op = OPS[tokens[i]]
    else:
      if tokens[i] == '(':
        right, i = eval_math(tokens, i + 1, do_last=do_last)
      elif tokens[i] == ')':
        if do_last:
          results.append(left)
          left = functools.reduce(OPS[do_last], results)
        return left, i
      else:
        right = tokens[i]
      if not do_last or op != OPS[do_last]:
        left = op(left, right)
      else:
        results.append(left)
        left = right
    i += 1
  if do_last:
    results.append(left)
    left = functools.reduce(OPS[do_last], results)
  return left


def part1(input):
  return sum(eval_math(line) for line in input)


def part2(input):
  return sum(eval_math(line, do_last='*') for line in input)


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
