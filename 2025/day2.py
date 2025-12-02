#!/usr/bin/env python

import functools
import os.path


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + ".txt"
  with open(filename) as fp:
    input = fp.read().rstrip("\n")

  return [tuple(map(int, r.split("-"))) for r in input.split(",")]


def find_illegal_ids(range_min, range_max, split=2):
  min_str = str(range_min)
  digits = len(min_str) // split + (1 if len(min_str) % split else 0)
  if digits * split > len(min_str):
    i = pow(10, digits - 1)
  else:
    i = int(min_str[:digits])
  n = int(str(i) * split)
  while n <= range_max:
    if n >= range_min:
      yield n
    i += 1
    n = int(str(i) * split)


def part1(input):
  return sum(
    sum(set(find_illegal_ids(range_min, range_max)))
    for range_min, range_max in input
  )


def part2(input):
  return sum(
    sum(
      functools.reduce(
        set.union,
        (
          set(find_illegal_ids(range_min, range_max, split))
          for split in range(2, len(str(range_max)) + 1)
        ),
        set(),
      )
    )
    for range_min, range_max in input
  )


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
