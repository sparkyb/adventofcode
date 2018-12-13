import os.path
import re
import math
from collections import defaultdict
import itertools
import md5


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0]+'.txt'
  with open(filename) as fp:
    input = fp.read().rstrip()

  map = input.split('\n')
  carts = []
  for y, row in enumerate(map):
    for x, cell in enumerate(row):
      if cell == '^':
        carts.append((y, x, -1, 0, 0))
        map[y] = map[y][:x] + '|' + map[y][x+1:]
      elif cell == 'v':
        carts.append((y, x, 1, 0, 0))
        map[y] = map[y][:x] + '|' + map[y][x+1:]
      elif cell == '<':
        carts.append((y, x, 0, -1, 0))
        map[y] = map[y][:x] + '-' + map[y][x+1:]
      elif cell == '>':
        carts.append((y, x, 0, 1, 0))
        map[y] = map[y][:x] + '-' + map[y][x+1:]
  return map, carts


def step(map, cart):
  y,x,dy,dx,turn = cart
  y += dy
  x += dx
  if map[y][x] == '/':
    dx, dy = -dy, -dx
  elif map[y][x] == '\\':
    dx, dy = dy, dx
  elif map[y][x] == '+':
    if turn == 0:
      if dx:
        dx, dy = -dy, -dx
      else:
        dx, dy = dy, dx
    elif turn == 2:
      if dy:
        dx, dy = -dy, -dx
      else:
        dx, dy = dy, dx
    turn = (turn + 1) % 3
  return (y, x, dy, dx, turn)

def collide(cart, carts, new_carts):
    y, x, dy, dx, turn = cart
    for j, cart in enumerate(carts):
      if y == cart[0] and x == cart[1]:
        del carts[j]
        return '%d,%d' % (x, y)
    for j, cart in enumerate(new_carts):
      if y == cart[0] and x == cart[1]:
        del new_carts[j]
        return '%d,%d' % (x, y)
    new_carts.append((y, x, dy, dx, turn))
    return None

def part1(input):
  map, carts = input
  carts = list(carts)
  while carts:
    carts.sort()
    new_carts = []
    while carts:
      cart = carts.pop(0)
      cart = step(map, cart)
      collision = collide(cart, carts, new_carts)
      if collision:
        return collision
    carts = new_carts

def part2(input):
  map, carts = input
  carts = list(carts)
  while carts:
    carts.sort()
    new_carts = []
    while carts:
      cart = carts.pop(0)
      cart = step(map, cart)
      collide(cart, carts, new_carts)
    carts = new_carts
    if len(carts) == 1:
      return '%d,%d' % (carts[0][1], carts[0][0])
  return None

if __name__ == '__main__':
  input = get_input()
  print part1(input)
  print part2(input)
