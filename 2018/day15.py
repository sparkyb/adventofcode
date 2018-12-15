import os.path
import re
import math
from collections import defaultdict
import itertools
import md5
import msvcrt
import sys

class Unit(object):
  def __init__(self,y,x,type):
    self.y = y
    self.x = x
    self.type = type

  def __cmp__(self,other):
    return cmp((self.y,self.x),(other.y,other.x))

  def __str__(self):
    return type

class Map(object):
  def __init__(self, map, attack={'E':3,'G':3}):
    self.map = list(map)
    self.units = {}
    for y, row in enumerate(self.map):
      for x, cell in enumerate(row):
        if cell in 'EG':
          self.units[(y, x)] = {'type':cell, 'hp':200, 'attack':attack[cell]}
          self.map[y] = self.map[y][:x] + '.' + self.map[y][x+1:]
    self.casualties = {'E':0, 'G':0}

  def order(self):
    return sorted(self.units.keys())

  def adjacent(self,cell):
    y, x = cell
    cells = [(y-1,x),(y,x-1),(y,x+1),(y+1,x)]
    for cell in cells:
      if cell in self.units:
        continue
      if (cell[0] >= 0 and cell[0] < len(self.map) and
          cell[1] >= 0 and cell[1] < len(self.map[cell[0]]) and 
          self.map[cell[0]][cell[1]] == '.'):
        yield cell

  def enemies(self, type):
    return [cell for cell, unit in self.units.items() if unit['type'] != type]

  def paths(self, cell):
    paths = {}
    frontier = [(cell2, [cell2]) for cell2 in self.adjacent(cell)]
    while frontier:
      cell, path = frontier.pop(0)
      if (cell not in paths or len(paths[cell]) > len(path) or
          (len(paths[cell]) == len(path) and paths[cell] > path)):
        paths[cell] = path
        frontier.extend((cell2, path + [cell2]) for cell2 in self.adjacent(cell))
    return paths

  def turn(self):
    order = self.order()
    for cell in order:
      if cell not in self.units:
        continue
      unit = self.units[cell]
      enemies = self.enemies(unit['type'])
      if not enemies:
        return False
      adjacent_enemies = [cell2 for cell2 in enemies if (cell[0]==cell2[0] and abs(cell[1]-cell2[1])==1) or (cell[1]==cell2[1] and abs(cell[0]-cell2[0])==1)]
      if (not adjacent_enemies):
        in_range = set()
        for cell2 in enemies:
          in_range.update(self.adjacent(cell2))
        if not in_range:
          continue
        paths = self.paths(cell)
        reachable = [cell2 for cell2 in in_range if cell2 in paths]
        if not reachable:
          continue
        reachable.sort(key=lambda c:(len(paths[c]),c))
        self.move(cell, paths[reachable[0]][0])
        cell = paths[reachable[0]][0]
      adjacent_enemies = [cell2 for cell2 in enemies if (cell[0]==cell2[0] and abs(cell[1]-cell2[1])==1) or (cell[1]==cell2[1] and abs(cell[0]-cell2[0])==1)]
      if adjacent_enemies:
        adjacent_enemies.sort(key=lambda c: (self.units[c]['hp'],c))
        self.attack(cell, adjacent_enemies[0])
    return True

  def move(self, from_cell, to_cell):
    assert from_cell in self.units
    assert to_cell not in self.units
    assert self.map[to_cell[0]][to_cell[1]] == '.'
    unit = self.units.pop(from_cell)
    self.units[to_cell] = unit

  def attack(self, from_cell, to_cell):
    assert from_cell in self.units
    assert to_cell in self.units
    assert self.units[from_cell]['type'] != self.units[to_cell]['type']
    self.units[to_cell]['hp'] -= self.units[from_cell]['attack']
    if self.units[to_cell]['hp'] <= 0:
      type = self.units[to_cell]['type']
      self.casualties[type] = self.casualties.get(type,0) + 1
      del self.units[to_cell]
      return type
    return ''

  def draw(self,turns):
    print 'After %d rounds:' % turns
    for y, row in enumerate(self.map):
      row_units = [self.units[(y,x)] for x in xrange(len(row)) if (y,x) in self.units]
      row = ''.join(self.units.get((y,x),{'type':cell})['type'] for x,cell in enumerate(row))
      print row + '   ' + ', '.join('%(type)s(%(hp)d)'%unit for unit in row_units)
    print

def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0]+'.txt'
  with open(filename) as fp:
    input = fp.read().rstrip()

  return input.split('\n')

def part1(map):
  map = Map(map)
  turns = 0
  ## map.draw(turns)
  ## if msvcrt.getch() == chr(27):
    ## sys.exit()
  while map.turn():
    turns += 1
    ## map.draw(turns)
    ## if msvcrt.getch() == chr(27):
      ## sys.exit()
  ## map.draw(turns)
  print 'Turns: %d' % turns
  return turns * sum(unit['hp'] for unit in map.units.values())

def part2(orig_map):
  attack={'E':3,'G':3}
  while True:
    attack['E'] += 1
    print 'Attack Power: %d' % attack['E']
    turns = 0
    map = Map(orig_map, attack)
    while map.turn():
      turns += 1
      if map.casualties['E']:
        break
    if not map.casualties['E']:
      print 'Turns: %d' % turns
      return turns * sum(unit['hp'] for unit in map.units.values())


if __name__ == '__main__':
  input = get_input()
  print part1(input)
  print part2(input)
