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

  lines = input.split('\n')
  initial = re.search(r'^initial state: ([\.#]+)$', lines[0]).group(1)
  rules = [re.search(r'^([\.#]{5}) => ([\.#])$', line).groups() for line in lines[2:]]
  rules = [(pattern,result) for pattern,result in rules if result == '#']
  return initial, rules


def step(pots, rules, offset=0):
  next_pots = ''
  pots = '....'+pots+'....'
  offset -= 4
  for i in xrange(pots.index('#') - 2, pots.rindex('#') + 3):
    segment = pots[i-2:i+3]
    for pattern, result in rules:
      if pattern == segment:
        if next_pots or result == '#':
          if not next_pots:
            offset += i
          next_pots += result
        break
    else:
      if next_pots:
        next_pots += '.'
      #raise ValueError("No pattern for %s" % segment)
  return next_pots.rstrip('.'), offset

def part1(input):
  pots, rules = input
  offset = 0
  for i in xrange(20):
    ## print offset, pots
    pots, offset = step(pots, rules, offset)
  return sum(i+offset for i, p in enumerate(pots) if p=='#')

def part2(input):
  pots, rules = input
  offset = 0
  n = 50000000000
  steps = [pots]
  offsets = [offset]
  while True:
    ## print offset, pots
    pots, offset = step(pots, rules, offset)
    if (pots in steps):
      loop = steps.index(pots)
      num_loops, i = divmod(n - loop, len(steps) - loop)
      i += loop
      pots = steps[i]
      offset = offsets[i] + (offset - offsets[loop]) * num_loops
      break
    else:
      steps.append(pots)
      offsets.append(offset)
      if len(steps) % 1000 == 0:
        print len(steps)
  return sum(i+offset for i, p in enumerate(pots) if p=='#')


if __name__ == '__main__':
  input = get_input()
  print part1(input)
  print part2(input)
