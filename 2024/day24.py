#!/usr/bin/env python

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

  wire_section, gate_section = input.split('\n\n')
  wires = {}
  gates = collections.defaultdict(list)
  for wire in wire_section.split('\n'):
    match  = re.search(r'^([a-z0-9]{3}): ([01])$', wire)
    wires[match[1]] = int(match[2])
  for gate in gate_section.split('\n'):
    match = re.search(
        r'^([a-z0-9]{3}) (AND|OR|XOR) ([a-z0-9]{3}) -> ([a-z0-9]{3})$',
        gate)
    gates[match[2]].append((frozenset((match[1], match[3])), match[4]))
  return gates, wires


OPS = {
  'XOR': operator.xor,
  'AND': operator.and_,
  'OR': operator.or_,
}


def part1(input):
  gates, wires = input
  wires = dict(wires)
  changed = True
  while changed:
    changed = False
    for op, items in gates.items():
      for inputs, output in items:
        if all(input in wires for input in inputs) and output not in wires:
          changed = True
          wires[output] = functools.reduce(OPS[op],
                                           (wires[wire] for wire in inputs))
  result = 0
  for wire, value in wires.items():
    if match := re.search(r'^z(\d{2})$', wire):
      result |= value << int(match[1])
  return result


def part2(input):
  gates, wires = input
  bits = max(int(wire[1:]) for wire in wires if wire.startswith('x')) + 1
  xor1 = [None] * bits
  and1 = [None] * bits
  xor2 = {}
  and2 = {}
  carry = {}
  for inputs, output in gates['XOR']:
    in1, in2 = sorted(inputs)
    if match := re.search(r'^x(\d{2})$', in1):
      bit = int(match[1])
      assert in2 == f'y{bit:02}'
      xor1[bit] = output
    else:
      xor2[in1] = output
      xor2[in2] = output
  for inputs, output in gates['AND']:
    in1, in2 = sorted(inputs)
    if match := re.search(r'^x(\d{2})$', in1):
      bit = int(match[1])
      assert in2 == f'y{bit:02}'
      and1[bit] = output
    else:
      and2[in1] = output
      and2[in2] = output
  for inputs, output in gates['OR']:
      in1, in2 = inputs
      carry[in1] = output
      carry[in2] = output

  errors = set()
  for bit, output in enumerate(xor1):
    if bit == 0:
      if output != 'z00':
        errors.add(output)
        errors.add('z00')
    elif output not in xor2:
      errors.add(output)
  for bit, output in enumerate(and1):
    if bit == 0:
      if output not in xor2:
        errors.add(output)
    elif output not in carry:
      errors.add(output)
  for output in xor2.values():
    if not re.match(r'^z(\d{2})$', output):
      errors.add(output)
  for output in and2.values():
    if output not in carry:
      errors.add(output)
  for output in carry.values():
    if output != f'z{bits:02}' and output not in xor2:
      errors.add(output)
  return ','.join(sorted(errors))


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
