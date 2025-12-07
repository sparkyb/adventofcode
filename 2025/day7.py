#!/usr/bin/env python

import bisect
import collections
import os.path


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + ".txt"
  with open(filename) as fp:
    input = fp.read().rstrip("\n")

  start = None
  columns = collections.defaultdict(list)
  for y, row in enumerate(input.split("\n")):
    for x, c in enumerate(row):
      if c == "S":
        start = (y, x)
      elif c == "^":
        columns[x].append(y)
  return start, columns


def find_splitter(start, columns):
  y, x = start
  i = bisect.bisect(columns[x], y)
  if i < len(columns[x]):
    y = columns[x][i]
    return y, x
  else:
    return None


def part1(input):
  start, columns = input
  used_splitters = set()
  beams = [start]
  while beams:
    splitter = find_splitter(beams.pop(), columns)
    if splitter and splitter not in used_splitters:
      used_splitters.add(splitter)
      beams.append((splitter[0], splitter[1] - 1))
      beams.append((splitter[0], splitter[1] + 1))

  return len(used_splitters)


def part2(input):
  start, columns = input
  splitters = [(y, x) for x, ys in columns.items() for y in ys]
  splitters.sort(reverse=True)
  num_below = collections.defaultdict(lambda: 1)
  for y, x in splitters:
    left = find_splitter((y, x - 1), columns)
    right = find_splitter((y, x + 1), columns)
    num_below[(y, x)] = num_below[left] + num_below[right]
  return num_below[find_splitter(start, columns)]


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
