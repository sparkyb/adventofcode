#!/usr/bin/env python

import functools
import operator
import os.path


OPERATIONS = {
  "+": operator.add,
  "*": operator.mul,
}


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + ".txt"
  with open(filename) as fp:
    input = fp.read().rstrip("\n")

  lines = input.split("\n")
  ops = [OPERATIONS[op] for op in lines[-1].split()]
  return (ops, lines[:-1])


def part1(input):
  ops, num_lines = input
  numbers = list(zip(*(list(map(int, line.split())) for line in num_lines)))
  return sum(functools.reduce(op, nums) for op, nums in zip(ops, numbers))


def part2(input):
  ops, num_lines = input
  transposed = " ".join("".join(col).strip() or "\n" for col in zip(*num_lines))
  numbers = [
    list(map(int, line.strip().split())) for line in transposed.split("\n")
  ]
  return sum(functools.reduce(op, nums) for op, nums in zip(ops, numbers))


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
