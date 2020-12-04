import collections
from collections import defaultdict
import enum
import functools
import itertools
import math
import msvcrt
import os.path
import re
import sys

#import numpy as np


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  records = []
  record = {}
  for line in input.split('\n'):
    if not line:
      records.append(record)
      record = {}
    else:
      for field in line.split(' '):
        k, v = field.split(':')
        record[k] = v
  if record:
    records.append(record)
  return records


FIELD_VALIDATION = {
    'byr': lambda field: field.isdigit() and 1920 <= int(field) <= 2002,
    'iyr': lambda field: field.isdigit() and 2010 <= int(field) <= 2020,
    'eyr': lambda field: field.isdigit() and 2020 <= int(field) <= 2030,
    'hgt': lambda field: (re.search(r'^(\d+)(in|cm)$', field) and
                          (150 <= int(field[:-2]) <= 193 if field[-2:] == 'cm'
                           else 59 <= int(field[:-2]) <= 76)),
    'hcl': lambda field: re.search('^#[0-9a-f]{6}$', field),
    'ecl': lambda field: field in ('amb','blu','brn','gry','grn','hzl','oth'),
    'pid': lambda field: re.search('^\d{9}$', field),
}


def part1(input):
  fields = set(FIELD_VALIDATION.keys())
  return sum(set(record.keys()) >= fields for record in input)


def part2(input):
  return sum(all(is_valid(record.get(field, ''))
                 for field, is_valid in FIELD_VALIDATION.items())
             for record in input)


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
