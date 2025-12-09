#!/usr/bin/env python

import itertools
import math
import os.path


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + ".txt"
  with open(filename) as fp:
    input = fp.read().rstrip("\n")

  return [tuple(map(int, line.split(","))) for line in input.split("\n")]


def area(a, b):
  return math.prod(abs(n - m) + 1 for n, m in zip(a, b))


def intersects(walls, lx, ly0, ly1):
  parity = 0
  side = -1
  for wy, (wx0, wx1) in walls:
    if wy >= ly1:
      break
    if wy > ly0 and side < 0:
      return True
    if lx < wx0 or lx > wx1:
      # line left or right of wall
      continue
    elif lx == wx0 or lx == wx1:
      # line hits the corner
      if side:
        parity = side * ((lx == wx0) * 2 - 1)
        side = 0
      else:
        side = parity * ((lx == wx0) * 2 - 1)
    else:
      side = -side
  return side < 0


def inside(corners, vertical_walls, horizontal_walls):
  (x0, y0), (x1, y1) = corners
  points = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
  for i, (x0, y0) in enumerate(points):
    x1, y1 = points[(i + 1) % len(points)]
    if x0 == x1:
      # vertical
      if intersects(horizontal_walls, x0, min(y0, y1), max(y0, y1)):
        return False
    else:
      assert y0 == y1
      # horizontal
      if intersects(vertical_walls, y0, min(x0, x1), max(x0, x1)):
        return False
  return True


def part1(input):
  return max(area(a, b) for a, b in itertools.combinations(input, 2))


def part2(input):
  vertical_walls = []
  horizontal_walls = []
  for i, (x0, y0) in enumerate(input):
    x1, y1 = input[(i + 1) % len(input)]
    if x0 == x1:
      # vertical
      vertical_walls.append((x0, (min(y0, y1), max(y0, y1))))
    else:
      assert y0 == y1
      # horizontal
      horizontal_walls.append((y0, (min(x0, x1), max(x0, x1))))
  vertical_walls.sort()
  horizontal_walls.sort()
  return max(
    area(a, b)
    for a, b in itertools.combinations(input, 2)
    if inside((a, b), vertical_walls, horizontal_walls)
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
