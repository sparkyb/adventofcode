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
    input = fp.read().strip()

  data = [int(n) for n in input.split(' ')]
  root, i = get_node(data)
  assert i == len(data)
  return root


def get_node(data, i=0):
  num_children = data[i]
  num_metadata = data[i + 1]
  i += 2
  node = {'children': [], 'metadata': []}
  for j in xrange(num_children):
    child, i = get_node(data, i)
    node['children'].append(child)
  node['metadata'] = data[i:i+num_metadata]
  return node, i+num_metadata

def part1(node):
  s = sum(node['metadata'], 0)
  for child in node['children']:
    s += part1(child)
  return s

def part2(node):
  if not node['children']:
    return sum(node['metadata'], 0)
  s = 0
  for i in node['metadata']:
    if i >= 1 and i <= len(node['children']):
      s += part2(node['children'][i-1])
  return s


if __name__ == '__main__':
  input = get_input()
  print part1(input)
  print part2(input)
