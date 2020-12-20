import collections
from collections import defaultdict
import enum
import functools
import itertools
import math
import msvcrt
import operator
import os.path
import re
import sys

import numpy as np


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  tiles = {}
  for tile in input.split('\n\n'):
    heading, *grid = tile.split('\n')
    tile_num = int(re.search(r'^Tile (\d+):$', heading).group(1))
    tiles[tile_num] = np.array([list(line) for line in grid])
  return arrange_tiles(tiles)


def orientations(tile):
  yield tile
  flipped = np.flipud(tile)
  yield flipped
  for k in range(1, 4):
    yield np.rot90(tile, k)
    yield np.rot90(flipped, k)


def tiles_match(tile1, tile2, axis):
  if axis == 0:
    return np.array_equal(tile1[-1, :], tile2[0, :])
  else:
    return np.array_equal(tile1[:, -1], tile2[:, 0])


def tile_fits(grid, tile, coord):
  return (
      (coord[0] == 0 or tiles_match(grid[coord[0] - 1, coord[1]], tile, 0)) and
      (coord[1] == 0 or tiles_match(grid[coord[0], coord[1] - 1], tile, 1)))


def arrange_tiles(tiles, grid=None, tile_nums=None, coord=(0, 0)):
  if grid is None:
    n = int(pow(len(tiles), .5))
    tile = next(iter(tiles.values()))
    if isinstance(tile, list):
      tile = tile[0]
    else:
      tiles = {tile_num: list(orientations(tile))
               for tile_num, tile in tiles.items()}
    grid = np.empty((n, n, *tile.shape), dtype=tile.dtype)
    tile_nums = np.full((n, n), -1)
  next_coord = (coord[0] + (coord[1] + 1) // tile_nums.shape[-1],
                (coord[1] + 1) % tile_nums.shape[-1])
  for tile_num, tile_orientations in tiles.items():
    for tile in tile_orientations:
      if tile_fits(grid, tile, coord):
        grid[coord] = tile
        tile_nums[coord] = tile_num
        new_tiles = dict(tiles)
        del new_tiles[tile_num]
        if (not new_tiles or
            arrange_tiles(new_tiles, grid, tile_nums, next_coord) is not None):
          grid = np.block([list(row) for row in grid[:, :, 1:-1, 1:-1]])
          return grid, tile_nums
  return None


def part1(input):
  _, tile_nums = input
  corners = list(map(int, tile_nums[np.ix_([0, -1], [0, -1])].flat))
  ## print(corners)
  return functools.reduce(operator.mul, corners)


def part2(input):
  grid, _ = input
  grids = list(orientations(grid))
  seamonster = [
      '                  # ',
      '#    ##    ##    ###',
      ' #  #  #  #  #  #   ',
  ]
  seamonster = np.array([[c == '#' for c in line] for line in seamonster])
  target = np.count_nonzero(seamonster)
  for grid in grids:
    count = 0
    for y in range(grid.shape[0] - seamonster.shape[0] + 1):
      for x in range(grid.shape[1] - seamonster.shape[1] + 1):
        index = (slice(y, y + seamonster.shape[0]),
                 slice(x, x + seamonster.shape[1]))
        if np.count_nonzero(seamonster & (grid[index] == '#')) == target:
          count += 1
          grid[index][np.where(seamonster)] = 'O'
    if count:
      ## print(count)
      return np.count_nonzero(grid == '#')


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
