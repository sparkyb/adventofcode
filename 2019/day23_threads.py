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
import threading

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
    self.lock = threading.RLock()
    self.part1 = None
    self.part1_event = threading.Event()
    self.nat = None
    self.prev_y = None
    self.part2 = None
    self.part2_event = threading.Event()

  def send(self, dest, x, y):
    with self.lock:
      ## print(dest, x, y)
      if dest == 255:
        if self.part1 is None:
          self.part1 = y
          self.part1_event.set()
        self.nat = [x, y]
      if 0 <= dest < len(self.computers):
        self.computers[dest].send(x, y)

  def update_empty(self):
    with self.lock:
      if all(comp.empty >= 2 for comp in self.computers):
        self.computers[0].send(*self.nat)
        y = self.nat[1]
        if y == self.prev_y and self.part2 is None:
          self.part2 = y
          self.part2_event.set()
        self.prev_y = y

  def run(self):
    for comp in self.computers:
      comp.start()



class Computer(threading.Thread):
  def __init__(self, controller, input, num):
    super().__init__()
    self.daemon = True
    self.controller = controller
    self.prog = Intcode(input, [num])
    self.lock = threading.RLock()
    self.empty = 0

  def send(self, x, y):
    with self.lock:
      self.empty = 0
      self.prog.input.extend([x, y])

  def run(self):
    while True:
      try:
        dest = self.prog.run(True)
      except NeedsInput:
        with self.lock:
          if not self.prog.input:
            self.prog.input.append(-1)
            self.empty += 1
        self.controller.update_empty()
      else:
        if dest is None:
          return
        x = self.prog.run(True)
        y = self.prog.run(True)
        self.controller.send(dest, x, y)


def part1(controller):
  controller.part1_event.wait()
  return controller.part1


def part2(controller):
  controller.part2_event.wait()
  return controller.part2


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  controller = Controller(input)
  controller.run()
  print(part1(controller))
  print(part2(controller))
