from collections import defaultdict
import enum
import itertools
import math
from hashlib import md5
import msvcrt
import numpy as np
import os.path
import re
import sys

from intcode import Intcode, NeedsInput


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip()

  return list(map(int, input.split(',')))


class Tile(enum.IntEnum):
  def __new__(cls, value, char):
    member = int.__new__(cls, value)
    member._value_ = value
    return member

  def __init__(self, value, char):
    self.char = char

  def __str__(self):
    return self.char

  EMPTY = (0, ' ')
  WALL = (1, '|')
  BLOCK = (2, '#')
  PADDLE = (3, '-')
  BALL = (4, 'o')


class Game:
  def __init__(self, input, play=False):
    self.prog = Intcode(input)
    if play:
      self.prog[0] = 2
    self.board = np.zeros((0, 0), dtype='u8')
    self.paddle = np.array([0, 0])
    self.ball = np.array([0, 0])
    self.score = 0
    self.blocks = 0

  def step(self):
    try:
      while True:
        x = self.prog.run(True)
        if x is None:
          return False
        y = self.prog.run(True)
        if x == -1 and y == 0:
          self.score = self.prog.run(True)
        else:
          tile = Tile(self.prog.run(True))
          if tile == Tile.PADDLE:
            self.paddle = np.array([x, y])
          elif tile == Tile.BALL:
            self.ball = np.array([x, y])
          if y >= self.board.shape[0] or x >= self.board.shape[1]:
            self.board.resize(np.maximum(self.board.shape, np.array([y, x]) + 1))
          self.board[y, x] = tile.value
    except NeedsInput:
      return True
    finally:
      self.blocks = np.sum(self.board == Tile.BLOCK.value)

  def draw_board(self):
    for line in self.board:
      print(''.join(str(Tile(tile)) for tile in line))

  def move(self, dir):
    self.prog.input.append(np.sign(dir))

  def play(self):
    prev_blocks = self.blocks
    prev_score = self.score
    while self.step():
      ## self.draw_board()
      ## print('Score: {}'.format(self.score))
      ## print('Blocks: {}'.format(self.blocks)
      ## print()
      if self.blocks != prev_blocks or self.score != prev_score:
        prev_blocks = self.blocks
        prev_score = self.score
        print('Blocks: {}, Score: {}'.format(self.blocks, self.score))
      self.move(self.ball[0] - self.paddle[0])
    ## self.draw_board()
    if self.blocks:
      print('There are still {} blocks left!'.format(self.blocks))
    return self.score


def part1(input):
  game = Game(input)
  game.step()
  game.draw_board()
  return game.blocks


def part2(input):
  game = Game(input, play=True)
  return game.play()


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
