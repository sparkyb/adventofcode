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

  return [(match.group(1), int(match.group(2))) for line in input.split('\n')
          for match in [re.search('^(\w{3}) ([+-]\d+)$', line)]]


def run(code):
  acc = 0
  ip = 0
  ips = set()
  while 0 <= ip < len(code):
    if ip in ips:
      raise ValueError(acc)
    ips.add(ip)
    op, arg = code[ip]
    if op == 'acc':
      acc += arg
    elif op == 'jmp':
      ip += arg
      continue
    ip += 1
  if ip == len(code):
    return acc
  raise ValueError(None)


def part1(input):
  try:
    run(input)
  except ValueError as exc:
    return exc.args[0]


def part2(input):
  for ip, (op, arg) in enumerate(input):
    try:
      if op == 'jmp':
        return run(input[:ip] + [('nop', arg)] + input[ip + 1:])
      elif op == 'nop':
        return run(input[:ip] + [('jmp', arg)] + input[ip + 1:])
    except ValueError:
      pass


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
