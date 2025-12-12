#!/usr/bin/env python

import functools
import itertools
import os.path
import re


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + ".txt"
  with open(filename) as fp:
    input = fp.read().rstrip("\n")

  sections = input.split("\n\n")

  presents = [
    frozenset(
      (x, y)
      for y, row in enumerate(section.split("\n")[1:])
      for x, c in enumerate(row)
      if c == "#"
    )
    for section in sections[:-1]
  ]

  trees = []
  for line in sections[-1].split("\n"):
    match = re.search(r"^(\d+)x(\d+):((?: \d+)+)$", line)
    assert match
    w, h, counts = match.groups()
    w = int(w)
    h = int(h)
    counts = list(map(int, counts.strip().split(" ")))
    trees.append(((w, h), counts))
  return presents, trees


@functools.cache
def rotate(present):
  return frozenset((2 - y, x) for x, y in present)


@functools.cache
def flip(present):
  return frozenset((2 - x, y) for x, y in present)


@functools.cache
def transformations(present):
  options = set()
  options.add(present)
  for _ in range(3):
    present = rotate(present)
    options.add(present)
  present = flip(present)
  options.add(present)
  for _ in range(3):
    present = rotate(present)
    options.add(present)
  return options


@functools.cache
def translate(present, dx, dy):
  return frozenset((x + dx, y + dy) for x, y in present)


@functools.cache
def fitspresents(presents, w, h, occupied=frozenset()):
  if not presents:
    return True
  if sum(len(present) for present in presents) + len(occupied) > w * h:
    return False

  present, *rest = presents
  rest = tuple(rest)
  for shape in transformations(present):
    for dx in range(w - 2):
      for dy in range(h - 2):
        placed = translate(shape, dx, dy)
        if placed & occupied:
          continue
        if fitspresents(rest, w, h, occupied | placed):
          return True
      #   else:
      #     break
      # else:
      #   continue
      # break
  return False


def part1(input):
  presents, trees = input
  print(
    sum(
      sum(len(present) * count for present, count in zip(presents, counts))
      <= w * h
      for (w, h), counts in trees
    )
  )
  ret = 0
  for i, ((w, h), counts) in enumerate(trees):
    if fitspresents(
      tuple(
        itertools.chain(
          *([present] * count for present, count in zip(presents, counts))
        )
      ),
      w,
      h,
    ):
      ret += 1
      print(f"{i + 1}/{len(trees)}: {w}x{h} fits")
    else:
      print(f"{i + 1}/{len(trees)}: {w}x{h} fails")
  return ret


def part2(input):
  return None


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
