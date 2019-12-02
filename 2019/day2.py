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

  return list(map(int,input.split(',')))

def intcode(input, noun, verb):
  mem = list(input)
  ip = 0
  mem[1] = noun
  mem[2] = verb

  while mem[ip] != 99:
    if mem[ip] == 1:
      mem[mem[ip + 3]] = mem[mem[ip + 1]] + mem[mem[ip + 2]]
    elif input[ip] == 2:
      mem[mem[ip + 3]] = mem[mem[ip + 1]] * mem[mem[ip + 2]]
    else:
      raise ValueError('Invalid opcode {} @ {}'.format(mem[ip], ip))
    ip += 4

  return mem[0]


def test(input):
  mem = list(input)
  ip = 0

  changed = defaultdict(set)
  while mem[ip] != 99:
    if ip in changed:
      raise ValueError('Opcode @ {} changed by {}'.format(
          ip,
          ', '.join(sorted(changed[ip]))))
    elif ip + 3 in changed:
      raise ValueError('Destination @ {} changed by {}'.format(
          ip + 3,
          ', '.join(sorted(changed[ip + 3]))))
    if mem[ip] not in (1, 2, 99):
      raise ValueError('Invalid opcode {} @ {}'.format(mem[ip], ip))
    if mem[ip + 1] < 0 or mem[ip + 1] >= len(mem):
      raise ValueError('Address {} is out of range @ {}'.format(mem[ip + 1], ip + 1))
    if mem[ip + 2] < 0 or mem[ip + 2] >= len(mem):
      raise ValueError('Address {} is out of range @ {}'.format(mem[ip + 2], ip + 2))
    if mem[ip + 3] < 0 or mem[ip + 3] >= len(mem):
      raise ValueError('Address {} is out of range @ {}'.format(mem[ip + 3], ip + 3))
    changed[mem[ip + 3]].add(ip + 3)
    ip += 4


def part1(input):
  return intcode(input, 12, 2)


def part2(input):
  for noun in range(100):
    for verb in range(100):
      if intcode(input, noun, verb) == 19690720:
        return 100 * noun + verb


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
