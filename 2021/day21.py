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


class PlayerState(collections.namedtuple('PlayerState', ('position', 'score'),
                                         defaults=(0,))):
  __slots__ = ()

  def move(self, amount):
    position = (self.position + amount - 1) % 10 + 1
    score = self.score + position
    return type(self)(position, score)


class GameState(tuple):
  __slots__ = ()

  def move(self, turn, amount):
    return type(self)(self[:turn] + (self[turn].move(amount),) + self[turn + 1:])


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  return GameState(PlayerState(int(line.split()[-1]))
                   for line in input.split('\n'))


def part1(state):
  rolls = 0
  die = itertools.cycle(range(1, 101))
  turn = 0
  while not any(player.score >= 1000 for player in state):
    state = state.move(turn, sum(next(die) for _ in range(3)))
    rolls += 3
    turn = 1 - turn
  return rolls * state[turn].score


def part2(state):
  states = collections.Counter((state,))

  rolls = collections.Counter(
      sum(rolls) for rolls in itertools.product(range(1, 4), repeat=3))

  turn = 0
  winners = [0, 0]
  while states:
    new_states = collections.Counter()
    for state, count in states.items():
      for amount, count2 in rolls.items():
        new_state = state.move(turn, amount)
        if new_state[turn].score >= 21:
          winners[turn] += count * count2
        else:
          new_states[new_state] += count * count2
    states = new_states
    turn = 1 - turn
  return max(winners)


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
