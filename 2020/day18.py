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


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  return input.split('\n')


OPS = {
    '+': operator.add,
    '*': operator.mul,
}


def tokenize(line):
  return [int(token) if token.isdigit() else token
           for token in re.findall(r'\d+|[(){}]'.format(''.join(OPS.keys())),
                                   line)]


def eval_math(tokens, i=0):
  left = 0
  op = operator.add
  while i < len(tokens):
    if tokens[i] in OPS:
      op = OPS[tokens[i]]
    else:
      if tokens[i] == '(':
        right, i = eval_math(tokens, i + 1)
      elif tokens[i] == ')':
        return left, i
      else:
        right = tokens[i]
      left = op(left, right)
    i += 1
  return left


def part1(input):
  return sum(eval_math(tokenize(line)) for line in input)


def part2(input):
  return sum(
      eval_math(tokenize(
          '(' +
          line.replace('(', '((').replace(')', '))').replace('*', ') * (') +
          ')'))
      for line in input)


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
