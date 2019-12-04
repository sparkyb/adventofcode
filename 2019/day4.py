from collections import defaultdict
import itertools
import math
from hashlib import md5
import msvcrt
import numpy as np
import os.path
import re
import sys


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip()

  return list(map(int, input.split('-')))


def has_doubles(digits, strict=False):
  if strict:
    return any(digits.count(d) == 2 for d in digits)
  else:
    return len(set(digits)) < len(digits)


def iterate_passwords(min_val, max_val, strict_doubles=False):
  count = 0
  for i in range(min_val, max_val + 1):
    digits = list(map(int, str(i)))
    if sorted(digits) == digits and has_doubles(digits, strict_doubles):
      count += 1
  return count


def digits_to_value(prefix, digits, extend):
  return int(''.join(str(d) for d in prefix + [extend] * (digits - len(prefix))))


def count_passwords(min_val, max_val, digits=6, prefix=[], strict_doubles=False):
  count = 0
  if not prefix:
    for d in range(min_val // pow(10, digits - 1), (max_val // pow(10, digits - 1)) + 1):
      count += count_passwords(min_val, max_val, digits, [d], strict_doubles)
  else:
    for d in range(prefix[-1], 10):
      new_prefix = prefix + [d]
      if (digits_to_value(new_prefix, digits, 9) < min_val or
          digits_to_value(new_prefix, digits, d) > max_val):
        continue
      if len(new_prefix) == digits:
        if has_doubles(new_prefix, strict_doubles):
          count += 1
      else:
        count += count_passwords(min_val, max_val, digits, new_prefix, strict_doubles)
  return count


def part1(input):
  min_val, max_val = input
  ## return iterate_passwords(min_val, max_val)
  return count_passwords(min_val, max_val)


def part2(input):
  min_val, max_val = input
  ## return iterate_passwords(min_val, max_val, strict_doubles=True)
  return count_passwords(min_val, max_val, strict_doubles=True)


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
