#!/usr/bin/env python

import bisect
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


Room = collections.namedtuple('Room', ('index', 'letter', 'x', 'step_cost'))

ROOM_Y = 2
ROOM_LETTERS = 'ABCD'
ROOMS = {l: Room(i, l, 3 + 2 * i, pow(10, i))
         for i, l in enumerate(ROOM_LETTERS)}
ROOM_X = {room.x for room in ROOMS.values()}


HALL_Y = 1
HALLS = [x for x in range(1, 12) if x not in ROOM_X]


PART2_LINES = [
    '  #D#C#B#A#',
    '  #D#B#A#C#',
]


class Map:
  @classmethod
  def from_string(cls, input):
    lines = input.split('\n')
    rooms = tuple(
        tuple(lines[y][room.x] for y in reversed(range(ROOM_Y, len(lines) - 1)))
        for room in ROOMS.values()
    )
    return cls(rooms)

  def __init__(self, rooms, halls=(None,) * len(HALLS), room_depth=None):
    if room_depth is None:
      room_depth = max(len(room) for room in rooms)
    self._rooms = rooms
    self._halls = halls
    self._room_depth = room_depth

  def __hash__(self):
    return hash((self._rooms, self._halls, self._room_depth))

  def __eq__(self, other):
    if not isinstance(other, Map):
      return NotImplemented
    return (self._rooms == other._rooms and self._halls == other._halls and
            self._room_depth == other._room_depth)

  @property
  def solved(self):
    return all(
        len(self._rooms[room.index]) == self._room_depth and
            all(l == room.letter for l in self._rooms[room.index])
        for room in ROOMS.values())

  def _can_move(self, from_x, to_x):
    if from_x < to_x:
      i = bisect.bisect_right(HALLS, from_x)
      j = bisect.bisect_right(HALLS, to_x)
    else:
      i = bisect.bisect_left(HALLS, to_x)
      j = bisect.bisect_left(HALLS, from_x)
    return not any(self._halls[i:j])

  def _room_ready(self, room):
    if isinstance(room, int):
      room = ROOM_LETTERS[room]
    if isinstance(room, str):
      room = ROOMS[room]
    return all(l == room.letter for l in self._rooms[room.index])

  @property
  def moves(self):
    for i, l in enumerate(self._halls):
      if not l:
        continue
      room = ROOMS[l]
      if self._room_ready(room) and self._can_move(HALLS[i], room.x):
        steps = (abs(room.x - HALLS[i]) +
                 self._room_depth - len(self._rooms[room.index]))
        energy = room.step_cost * steps
        new_halls = self._halls[:i] + (None,) + self._halls[i + 1:]
        new_rooms = (self._rooms[:room.index] +
                     (self._rooms[room.index] + (l,),) +
                     self._rooms[room.index + 1:])
        yield type(self)(new_rooms, new_halls, self._room_depth), energy
    for room in ROOMS.values():
      if self._room_ready(room):
        continue
      l = self._rooms[room.index][-1]
      for i, x in enumerate(HALLS):
        if self._can_move(room.x, x):
          steps = (abs(room.x - x) +
                   self._room_depth - len(self._rooms[room.index]) + 1)
          energy = ROOMS[l].step_cost * steps
          new_halls = self._halls[:i] + (l,) + self._halls[i + 1:]
          new_rooms = (self._rooms[:room.index] +
                       (self._rooms[room.index][:-1],) +
                       self._rooms[room.index + 1:])
          yield type(self)(new_rooms, new_halls, self._room_depth), energy


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  return input


@functools.lru_cache(maxsize=None)
def solve(map):
  if map.solved:
    return 0
  least_energy = None
  for new_map, energy in map.moves:
    total_energy = solve(new_map)
    if total_energy is not None:
      total_energy += energy
      if least_energy is None or total_energy < least_energy:
        least_energy = total_energy
  return least_energy


def part1(input):
  return solve(Map.from_string(input))


def part2(input):
  lines = input.split('\n')
  input = '\n'.join(lines[:3] + PART2_LINES + lines[3:])
  return solve(Map.from_string(input))


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
