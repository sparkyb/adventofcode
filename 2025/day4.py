#!/usr/bin/env python

import os.path


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + ".txt"
  with open(filename) as fp:
    input = fp.read().rstrip("\n")

  return frozenset(
    (y, x)
    for y, row in enumerate(input.split("\n"))
    for x, c in enumerate(row)
    if c == "@"
  )


def neighbors(y, x):
  return frozenset(
    (y + dy, x + dx)
    for dy in (-1, 0, 1)
    for dx in (-1, 0, 1)
    if dy != 0 or dx != 0
  )


def count_neighbors(rolls, y, x):
  return sum(1 for (y2, x2) in neighbors(y, x) if (y2, x2) in rolls)


def part1(input):
  return sum(1 for (y, x) in input if count_neighbors(input, y, x) < 4)


def part2(input):
  prev_rolls = frozenset()
  rolls = input
  while rolls != prev_rolls:
    prev_rolls = rolls
    rolls = frozenset(
      (y, x) for (y, x) in rolls if count_neighbors(rolls, y, x) >= 4
    )
  return len(input) - len(rolls)


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
