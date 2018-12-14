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

  return int(input)


def part1(input):
  scores = [3, 7]
  elves = [0, 1]
  while len(scores) < input + 10:
    sum = scores[elves[0]]+scores[elves[1]]
    scores.extend(map(int,str(sum)))
    for i, index in enumerate(elves):
      elves[i] = (index+scores[index]+1)%len(scores)
  return int(''.join(map(str,scores[input:input+10])))

def part2(input):
  scores = [3, 7]
  elves = [0, 1]
  input = map(int,str(input))
  while True:
    sum = scores[elves[0]]+scores[elves[1]]
    for score in map(int,str(sum)):
      scores.append(score)
      if scores[-len(input):] == input:
        return len(scores) - len(input)
    for i, index in enumerate(elves):
      elves[i] = (index+scores[index]+1)%len(scores)


if __name__ == '__main__':
  input = get_input()
  print part1(input)
  print part2(input)
