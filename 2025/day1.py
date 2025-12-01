#!/usr/bin/env python

import itertools
import os.path


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + ".txt"
  with open(filename) as fp:
    input = fp.read().rstrip("\n")

  return [
    int(line[1:]) * ((line[0] == "R") * 2 - 1) for line in input.split("\n")
  ]


def part1(input: list[int]):
  def modsum(acc: int, delta: int) -> int:
    return (acc + delta) % 100

  nums = itertools.accumulate(input, modsum, initial=50)
  return sum(num == 0 for num in nums)


def part2(input):
  count = 0
  prev = 50
  for delta in input:
    num = prev + delta
    diff = max(prev, num) - min(prev, num)
    count += diff // 100  # full rotations
    diff %= 100
    count += (
      (min(prev, num) % 100) + diff
    ) > 100  # partial rotation crosses 100
    prev = num % 100
    if diff:
      count += prev == 0  # lands on 100
  return count


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
