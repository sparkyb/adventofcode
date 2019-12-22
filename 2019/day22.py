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

  ops = []
  for line in input.split('\n'):
    match = re.search('^deal into new stack$', line)
    if match:
      ops.append(('reverse', 0))
      continue
    match = re.search('^cut (-?\d+)$', line)
    if match:
      cut = int(match.group(1))
      ops.append(('cut', cut))
      continue
    match = re.search('^deal with increment (\d+)$', line)
    if match:
      inc = int(match.group(1))
      ops.append(('deal', inc))
      continue
    raise ValueError('Unknown command: {}'.format(line))
  return ops


def flatten(ops, mod):
  deal = 1
  cut = 0
  for op, amount in ops:
    if op == 'reverse':
      deal = -deal % mod
      cut = (1 - cut) % mod
    elif op == 'cut':
      cut = (cut + amount) % mod
    elif op == 'deal':
      cut = (cut * amount) % mod
      deal = (deal * amount) % mod
    else:
      raise ValueError('Unknown op: {}'.format(op))
  return (deal, cut)


def extended_gcd(a, b):
  if a == 0:
    return (b, 0, 1)
  g, y, x = extended_gcd(b % a, a)
  return (g, x - (b // a) * y, y)


def modinv(a, m):
  g, x, y = extended_gcd(a, m)
  if g != 1:
    raise ValueError('No modular inverse')
  return x % m


def geo_sum(a, n, m):
  return ((pow(a, n + 1, m) - 1) * modinv(a - 1, m)) % m


def moddiv(a, b, m):
  return (a * modinv(b, m)) % m


def part1(input):
  n = 10007
  stack = list(range(n))
  deal, cut = flatten(input, n)
  stack = [stack[moddiv(i, deal, n)] for i in range(n)]
  stack = stack[cut:] + stack[:cut]
  ## print(' '.join(map(str, stack)))
  ## print(stack.index(2019))
  return (2019 * deal - cut) % n


def part2(input):
  n = 119315717514047
  e = 101741582076661
  deal, cut = flatten(input, n)
  cut = (cut * geo_sum(deal, e - 1, n)) % n
  deal = pow(deal, e, n)
  return moddiv(cut + 2020, deal, n)


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
