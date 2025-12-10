#!/usr/bin/env python

import functools
import itertools
import os.path
import re
import typing

import z3


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + ".txt"
  with open(filename) as fp:
    input = fp.read().rstrip("\n")

  machines = []
  for line in input.split("\n"):
    match = re.search(
      r"^\[([#\.]+)\]((?: \(\d+(?:,\d+)*\))+) \{(\d+(?:,\d+)*)\}$", line
    )
    assert match
    lights, buttons, joltages = match.groups()
    lights = frozenset(i for i, c in enumerate(lights) if c == "#")
    buttons = tuple(
      frozenset(map(int, button[1:-1].split(",")))
      for button in buttons.strip().split(" ")
    )
    joltages = tuple(map(int, joltages.split(",")))
    machines.append((lights, buttons, joltages))
  return machines


def min_lights(lights, buttons):
  for i in range(len(buttons) + 1):
    for subset in itertools.combinations(buttons, i):
      if functools.reduce(set.symmetric_difference, subset, set()) == lights:
        return i
  raise Exception("Couldn't find button set")


def part1(input):
  return sum(min_lights(lights, buttons) for lights, buttons, _ in input)


def min_joltages(joltages, buttons):
  presses = z3.IntVector("button", len(buttons))
  s = z3.Optimize()
  for p in presses:
    s.add(p >= 0)
  for i, j in enumerate(joltages):
    s.add(sum(p for p, b in zip(presses, buttons) if i in b) == j)
  s.minimize(sum(presses))
  assert s.check() == z3.sat
  m = s.model()
  return typing.cast(z3.IntNumRef, m.evaluate(sum(presses))).as_long()


def part2(input):
  return sum(min_joltages(joltages, buttons) for _, buttons, joltages in input)


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
