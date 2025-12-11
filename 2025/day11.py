#!/usr/bin/env python

import collections
import functools
import os.path


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + ".txt"
  with open(filename) as fp:
    input = fp.read().rstrip("\n")

  connections = collections.defaultdict(set)
  for line in input.split("\n"):
    machine, outputs = line.split(": ")
    connections[machine].update(outputs.split(" "))
  return connections


def part1(input):
  @functools.cache
  def count_paths(start):
    if start == "out":
      return 1
    return sum(count_paths(next) for next in input[start])

  return count_paths("you")


def part2(input):
  @functools.cache
  def count_paths(start, fft=False, dac=False):
    if start == "out":
      return 1 if fft and dac else 0
    return sum(
      count_paths(next, fft=fft or start == "fft", dac=dac or start == "dac")
      for next in input[start]
    )

  return count_paths("svr")


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
