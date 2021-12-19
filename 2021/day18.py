#!/usr/bin/env python

import collections
import collections.abc
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


class SnailfishTerm:
  def __init__(self, value, depth=0):
    self.value = int(value)
    self.depth = depth

  def __int__(self):
    return self.value

  def __add__(self, other):
    return type(self)(self.value + int(other), depth=self.depth)

  def __str__(self):
    return str(self.value)

  def __repr__(self):
    return f'{type(self).__name__}({self.value!r}, depth={self.depth!r})'


class SnailfishNumber:
  @classmethod
  def parse(cls, s):
    terms = []
    depth = 0
    n = None
    for c in s:
      if c in ',]' and n is not None:
        terms.append(SnailfishTerm(n, depth))
        n = None
      if c == '[':
        assert n is None
        depth += 1
      elif c == ']':
        assert n is None
        depth -= 1
      elif c.isdigit():
        if n is None:
          n = 0
        n = n * 10 + int(c)
    assert depth == 0
    return cls(terms)

  def __init__(self, terms):
    if isinstance(terms, SnailfishNumber):
      terms = list(terms._terms)
    elif isinstance(terms, int):
      terms = [SnailfishTerm(terms)]
    else:
      terms = list(terms)
    assert len(terms) > 0
    assert all(isinstance(term, SnailfishTerm) for term in terms)
    self._terms = terms

  def __str__(self):
    ret = ''
    stack = []
    for term in self._terms:
      assert not stack or stack[-1] < 2
      while term.depth > len(stack):
        ret += '['
        stack.append(0)
      assert term.depth == len(stack)
      ret += str(term)
      if stack:
        stack[-1] += 1
        if stack[-1] == 1:
          ret += ','
      while stack and stack[-1] == 2:
        ret += ']'
        stack.pop()
        if stack:
          stack[-1] += 1
          if stack[-1] == 1:
            ret += ','
    return ret

  def __add__(self, other):
    if isinstance(other, int):
      other = SnailfishNumber(other)
    if not isinstance(other, SnailfishNumber):
      raise TypeError(f'unsupported operand type(s) for +: '
                      '{type(self).__name__!r} and {type(other).__name__!r}')
    terms = [SnailfishTerm(term, term.depth + 1) for term in self._terms]
    terms.extend(SnailfishTerm(term.value, term.depth + 1) for term in other._terms)
    return type(self)(terms)._reduce()

  def __radd__(self, other):
    if isinstance(other, int):
      other = SnailfishNumber(other)
    if not isinstance(other, SnailfishNumber):
      raise TypeError(f'unsupported operand type(s) for +: '
                      '{type(other).__name__!r} and {type(self).__name__!r}')
    return other + self

  def _explode(self):
    for i, term in enumerate(self._terms):
      if term.depth > 4:
        assert self._terms[i + 1].depth == term.depth
        next_term = self._terms[i + 1]
        self._terms[i:i + 2] = [SnailfishTerm(0, term.depth - 1)]
        if i > 0:
          self._terms[i - 1].value += term.value
        if i + 1 < len(self._terms):
          self._terms[i + 1].value += next_term.value
        return True
    return False

  def _split(self):
    for i, term in enumerate(self._terms):
      if term.value >= 10:
        self._terms[i:i + 1] = [
            SnailfishTerm(math.floor(term.value / 2), term.depth + 1),
            SnailfishTerm(math.ceil(term.value / 2), term.depth + 1),
        ]
        return True
    return False

  def _reduce(self):
    while True:
      if self._explode():
        continue
      if self._split():
        continue
      break
    return self

  @property
  def magnitude(self):
    ret = 0
    stack = []
    for term in self._terms:
      assert not stack or stack[-1] < 2
      while term.depth > len(stack):
        stack.append(0)
      assert term.depth == len(stack)
      factor = math.prod((3, 2)[side] for side in stack)
      ret += term.value * factor
      if stack:
        stack[-1] += 1
      while stack and stack[-1] == 2:
        stack.pop()
        if stack:
          stack[-1] += 1
    return ret


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  return [SnailfishNumber.parse(line) for line in input.split('\n')]


def part1(input):
  return sum(input[1:], input[0]).magnitude


def part2(input):
  return max((num + num2).magnitude
             for num, num2 in itertools.permutations(input, 2))


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('-c', '--clip', '--copy', action='store_true',
                      help='Copy answer to clipboard')
  parser.add_argument('-p', '--part', type=int, choices=(1, 2),
                      help='Which part to run (default: both)')
  parser.add_argument('-1', '--part1', action='store_const', dest='part',
                      const=1, help='Part 1 only')
  parser.add_argument('-2', '--part2', action='store_const', dest='part',
                      const=2, help='Part 2 only')
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  if args.clip:
    import pyperclip
  input = get_input(args.input)
  if not args.part or args.part == 1:
    answer1 = part1(input)
    print(answer1)
    if args.clip and answer1 is not None:
      pyperclip.copy(str(answer1))
  if not args.part or args.part == 2:
    answer2 = part2(input)
    print(answer2)
    if args.clip and answer2 is not None:
      pyperclip.copy(str(answer2))
