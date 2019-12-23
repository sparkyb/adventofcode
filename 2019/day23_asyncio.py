import asyncio
import collections
from collections import defaultdict
import enum
import functools
import itertools
import math
import msvcrt
import os.path
import pdb
import re
import sys

#import numpy as np

from intcode import Intcode, NeedsInput


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  return list(map(int, input.split(',')))


class Controller:
  def __init__(self, input, num=50):
    self.computers = [Computer(self, input, i) for i in range(num)]
    self.nat = None
    self.prev_y = None
    self.part1 = asyncio.Future()
    self.part2 = asyncio.Future()

  def send(self, dest, x, y):
    ## print(dest, x, y)
    if dest == 255:
      self.nat = [x, y]
      if not self.part1.done():
        self.part1.set_result(y)
    if 0 <= dest < len(self.computers):
      self.computers[dest].send(x, y)

  def update_empty(self):
    if all(comp.empty >= 2 for comp in self.computers):
      self.computers[0].send(*self.nat)
      y = self.nat[1]
      if y == self.prev_y and not self.part2.done():
        self.part2.set_result(y)
      self.prev_y = y

  async def run(self):
    await asyncio.gather(*(comp.run() for comp in self.computers))


class Computer:
  def __init__(self, controller, input, num):
    self.controller = controller
    self.prog = Intcode(input, [num])
    self.queue = asyncio.Queue()
    self.empty = 0

  def send(self, x, y):
    self.queue.put_nowait(x)
    self.queue.put_nowait(y)

  async def run(self):
    while True:
      try:
        dest = self.prog.run(True)
      except NeedsInput:
        if self.queue.empty():
          self.empty += 1
          self.controller.update_empty()
          if self.empty >= 2:
            self.prog.input.append(await self.queue.get())
            self.empty = 0
          else:
            self.prog.input.append(-1)
        else:
          self.empty = 0
          while not self.queue.empty():
            self.prog.input.append(self.queue.get_nowait())
      else:
        if dest is None:
          return
        x = self.prog.run(True)
        y = self.prog.run(True)
        self.controller.send(dest, x, y)
      await asyncio.sleep(0)


def part1(input):
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  controller = Controller(input)
  task = asyncio.ensure_future(controller.run())
  try:
    return loop.run_until_complete(controller.part1)
  finally:
    task.cancel()
    try:
      loop.run_until_complete(task)
    except asyncio.CancelledError:
      pass
    loop.stop()
    loop.close()


def part2(input):
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  controller = Controller(input)
  task = asyncio.ensure_future(controller.run())
  try:
    return loop.run_until_complete(controller.part2)
  finally:
    task.cancel()
    try:
      loop.run_until_complete(task)
    except asyncio.CancelledError:
      pass
    loop.stop()
    loop.close()


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
