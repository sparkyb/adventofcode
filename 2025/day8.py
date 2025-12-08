#!/usr/bin/env python

import itertools
import math
import os.path


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + ".txt"
  with open(filename) as fp:
    input = fp.read().rstrip("\n")

  return frozenset(
    tuple(map(int, line.split(","))) for line in input.split("\n")
  )


def find(connections, coord):
  path = set()
  while isinstance(connections[coord], tuple):
    path.add(coord)
    coord = connections[coord]
  for mid in path:
    connections[mid] = coord
  return coord


def union(connections, a, b):
  a = find(connections, a)
  b = find(connections, b)
  if a != b:
    connections[b] += connections[a]
    connections[a] = b
  return connections[b]


def distance(a, b):
  return math.sqrt(sum(pow(n - m, 2) for n, m in zip(a, b)))


def part1(input):
  connections = {coord: 1 for coord in input}
  pairs = [(distance(a, b), a, b) for a, b in itertools.combinations(input, 2)]
  pairs.sort()
  for i in range(1000):
    _, a, b = pairs.pop(0)
    union(connections, a, b)
  sizes = [value for value in connections.values() if isinstance(value, int)]
  sizes.sort()
  return math.prod(sizes[-3:])


def part2(input):
  connections = {coord: 1 for coord in input}
  pairs = [(distance(a, b), a, b) for a, b in itertools.combinations(input, 2)]
  pairs.sort()
  while True:
    _, a, b = pairs.pop(0)
    if union(connections, a, b) == len(input):
      return a[0] * b[0]


if __name__ == "__main__":
  from argparse import ArgumentParser

  parser = ArgumentParser()
  parser.add_argument(
    "-c",
    "--clip",
    "--copy",
    action="store_true",
    help="Copy answer to clipboard",
  )
  parser.add_argument(
    "-p",
    "--part",
    type=int,
    choices=(1, 2),
    help="Which part to run (default: both)",
  )
  parser.add_argument(
    "-1",
    "--part1",
    action="store_const",
    dest="part",
    const=1,
    help="Part 1 only",
  )
  parser.add_argument(
    "-2",
    "--part2",
    action="store_const",
    dest="part",
    const=2,
    help="Part 2 only",
  )
  parser.add_argument("input", nargs="?", metavar="input.txt")
  args = parser.parse_args()
  if args.clip:
    import pyperclip
  input = get_input(args.input)
  if not args.part or args.part == 1:
    answer1 = part1(input)
    print(answer1)
    if args.clip and answer1 is not None:
      pyperclip.copy(str(answer1))  # type: ignore
  if not args.part or args.part == 2:
    answer2 = part2(input)
    print(answer2)
    if args.clip and answer2 is not None:
      pyperclip.copy(str(answer2))  # type: ignore
