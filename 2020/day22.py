import collections
from collections import defaultdict
import copy
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

  return tuple(tuple(map(int, section.split('\n')[1:]))
               for section in input.split('\n\n'))


@functools.lru_cache(maxsize=None)
def combat(players, recursive=False):
  history = set()
  while all(players):
    if recursive:
      if players in history:
        return 0, None
      history.add(players)
    cards = [player[0] for player in players]
    players = tuple(player[1:] for player in players)
    if (recursive and
        all(len(player) >= card for player, card in zip(players, cards))):
      winner, _ = combat(
          tuple(player[:card] for player, card in zip(players, cards)),
          recursive=True)
    else:
      winner = max(range(len(cards)), key=lambda index: cards[index])
    players = tuple(
        player + (cards[winner], cards[1 - winner]) if winner == i else player
        for i, player in enumerate(players))
  winner = max(range(len(players)), key=lambda index: len(players[index]))
  return winner, players[winner]


def part1(input):
  _, cards = combat(input)
  return sum(i * card for i, card in enumerate(reversed(cards), start=1))


def part2(input):
  _, cards = combat(input, recursive=True)
  return sum(i * card for i, card in enumerate(reversed(cards), start=1))


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
