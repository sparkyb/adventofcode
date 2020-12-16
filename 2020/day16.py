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

  in_fields = True
  fields = {}
  tickets = []
  for line in input.split('\n'):
    if not line:
      in_fields = False
      continue
    if in_fields:
      match = re.search(r'^([^:]+): (\d+)-(\d+) or (\d+)-(\d+)$', line)
      fields[match.group(1)] = [(int(match.group(2)), int(match.group(3))),
                                (int(match.group(4)), int(match.group(5)))]
    else:
      if re.search(r'^\d+(,\d+)*$', line):
        tickets.append(list(map(int, line.split(','))))
  return fields, tickets


def field_valid(num, ranges):
  for n, x in ranges:
    if n <= num <= x:
      return True
  return False


def ticket_valid(ticket, fields, ordered=False):
  if ordered:
    return all(field_valid(num, ranges) for num, ranges in zip(ticket, fields))
  else:
    return all(any(field_valid(num, ranges) for ranges in fields)
               for num in ticket)


def part1(input):
  fields, tickets = input
  error = 0
  for ticket in tickets[1:]:
    for num in ticket:
      if not any(field_valid(num, ranges) for ranges in fields.values()):
        error += num
  return error


def part2(input):
  fields, tickets = input
  valid_tickets = [ticket for ticket in tickets
                   if ticket_valid(ticket, fields.values())]

  field_sets = [set(field for field, ranges in fields.items()
                    if all(field_valid(num, ranges) for num in field_nums))
                for field_nums in zip(*valid_tickets)]

  field_order = [None] * len(field_sets)
  while True:
    for i, field_set in enumerate(field_sets):
      if len(field_set) == 1:
        field = list(field_set)[0]
        field_order[i] = field
        for field_set2 in field_sets:
          field_set2.discard(field)
        break
    else:
      break

  ## print(field_order)
  ticket = dict(zip(field_order, tickets[0]))
  ## print(ticket)
  return functools.reduce(
      operator.mul,
      (num for field, num in ticket.items() if field.startswith('departure')),
      1)


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
