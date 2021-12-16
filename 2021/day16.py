#!/usr/bin/env python

import collections
import collections.abc
from collections import defaultdict
import enum
import functools
import io
import itertools
import math
import msvcrt
import operator
import os.path
import re
import sys

#import numpy as np


class BitStream:
  def __init__(self, hex):
    self._stream = io.BytesIO(bytes.fromhex(hex))
    self._buf = 0
    self._bits = 0

  def tell(self):
    return self._stream.tell() * 8 - self._bits

  def read(self, bits):
    n = 0
    while bits:
      if not self._bits:
        self._buf = self._stream.read(1)[0]
        self._bits = 8
      if bits < self._bits:
        n <<= bits
        n |= (self._buf >> (self._bits - bits)) & ((1 << bits) - 1)
        self._bits -= bits
        bits = 0
      else:
        n << self._bits
        n |= self._buf & ((1 << self._bits) - 1)
        bits -= self._bits
        self._bits = 0
    return n


class PacketType(enum.IntEnum):
  SUM = 0
  PRODUCT = 1
  MIN = 2
  MAX = 3
  LITERAL = 4
  GT = 5
  LT = 6
  EQ = 7


class Packet(collections.abc.Sequence):
  def __init__(self, stream, depth=0):
    self.version = stream.read(3)
    self.type_id = PacketType(stream.read(3))
    self._value = None
    self._children = []
    if self.type_id == PacketType.LITERAL:
      self._value = 0
      more = True
      while more:
        more = stream.read(1)
        self._value <<= 4
        self._value |= stream.read(4)
    else:
      length_type = stream.read(1)
      if length_type == 0:
        length = stream.read(15)
        end = stream.tell() + length
        while stream.tell() < end:
          self._children.append(Packet(stream, depth=depth + 1))
      else:
        for _ in range(stream.read(11)):
          self._children.append(Packet(stream, depth=depth + 1))

  def __len__(self):
      return len(self._children)

  def __getitem__(self, index):
    return self._children[index]

  def __iter__(self):
    return iter(self._children)

  def __int__(self):
    return self.value

  @property
  def value(self):
    if self._value is None:
      if self.type_id == PacketType.SUM:
        self._value = sum(child.value for child in self)
      elif self.type_id == PacketType.PRODUCT:
        self._value = math.prod(child.value for child in self)
      elif self.type_id == PacketType.MIN:
        self._value = min(child.value for child in self)
      elif self.type_id == PacketType.MAX:
        self._value = max(child.value for child in self)
      elif self.type_id == PacketType.GT:
        self._value = int(self[0].value > self[1].value)
      elif self.type_id == PacketType.LT:
        self._value = int(self[0].value < self[1].value)
      elif self.type_id == PacketType.EQ:
        self._value = int(self[0].value == self[1].value)
    return self._value

  def iter_rec(self, depth_first=False):
    q = collections.deque([self])
    while q:
      packet = q.popleft()
      yield packet
      if depth_first:
        q.extendleft(reversed(packet))
      else:
        q.extend(packet)


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  return Packet(BitStream(input))


def part1(packet):
  return sum(p.version for p in packet.iter_rec())


def part2(packet):
  return packet.value


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
