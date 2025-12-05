#!/usr/bin/env python


import bisect
import os.path

# import numpy as np


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + ".txt"
  with open(filename) as fp:
    input = fp.read().rstrip("\n")

  fresh_section, available_section = input.split("\n\n")
  fresh_ranges = [
    tuple(map(int, line.split("-"))) for line in fresh_section.split("\n")
  ]
  available = list(map(int, available_section.split("\n")))
  return fresh_ranges, available


def part1(input):
  fresh_ranges, available = input
  return sum(
    1
    for ingredient in available
    if any(left <= ingredient <= right for left, right in fresh_ranges)
  )


def part2(input):
  fresh_ranges, _ = input
  unique_ranges = []
  for left, right in fresh_ranges:
    index = bisect.bisect(unique_ranges, (left, right))
    if index > 0 and unique_ranges[index - 1][1] >= left:
      left = unique_ranges[index - 1][0]
      right = max(right, unique_ranges[index - 1][1])
      del unique_ranges[index - 1]
      index -= 1
    while index < len(unique_ranges) and unique_ranges[index][0] <= right:
      right = max(right, unique_ranges[index][1])
      del unique_ranges[index]
    unique_ranges.insert(index, (left, right))
  return sum(x - n + 1 for n, x in unique_ranges)


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
