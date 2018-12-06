import os.path
import re
import math
from collections import defaultdict
import itertools
import md5
import sys


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0]+'.txt'
  with open(filename) as fp:
    input = fp.read().strip()

  return [map(lambda n: int(n.strip()),line.split(',')) for line in input.split('\n')]


def get_bounding_box(coords):
  box = [coords[0][0], coords[0][1], coords[0][0], coords[0][1]]
  for x, y in coords[1:]:
    if x < box[0]:
      box[0] = x
    elif x > box[2]:
      box[2] = x
    if y < box[1]:
      box[1] = y
    elif y > box[3]:
      box[3] = y
  return box


def part1(coords):
  box = get_bounding_box(coords)
  counts = {}
  onborder = set()
  for y in xrange(box[1],box[3]+1):
    for x in xrange(box[0],box[2]+1):
      closest_index = None
      closest_dist = None
      for i,coord in enumerate(coords):
        distance = abs(x-coord[0])+abs(y-coord[1])
        if closest_dist is None or distance < closest_dist:
          closest_index = i
          closest_dist = distance
        elif distance == closest_dist:
          closest_index = None
      if closest_index is not None:
        ## if x == coords[closest_index][0] and y == coords[closest_index][1]:
          ## sys.stdout.write(chr(closest_index+ord('A')))
        ## else:
          ## sys.stdout.write(chr(closest_index+ord('a')))
        if x == box[0] or x == box[2] or y == box[1] or y == box[3]:
          onborder.add(closest_index)
        else:
          counts[closest_index] = counts.get(closest_index, 0) + 1
      ## else:
        ## sys.stdout.write('.')
    ## sys.stdout.write('\n')
  ## print counts
  for i in onborder:
    if i in counts:
      del counts[i]
  return max(counts.values()) if counts else 0

def tri(n):
  return (n * (n + 1)) / 2


def total_distance(coords, x, y):
  distance = 0
  for coord in coords:
    distance += abs(x-coord[0])+abs(y-coord[1])
  return distance


def part2(coords):
  box = get_bounding_box(coords)
  threshold = 10000
  count = 0

  ## tried = set()
  ## totry = list(coords)
  ## while totry:
    ## x, y = totry.pop(0)
    ## c = (x, y)
    ## if c in tried:
      ## continue
    ## tried.add(c)
    ## distance = total_distance(coords, x, y)
    ## if distance < threshold:
      ## count += 1
      ## totry.extend([(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
  ## return count

  for y in xrange(box[1],box[3]+1):
    for x in xrange(box[0],box[2]+1):
      distance = 0
      for coord in coords:
        distance += abs(x-coord[0])+abs(y-coord[1])
        if distance >= threshold:
          break
      if distance < threshold:
        r = (threshold-distance-1)/len(coords) + 1
        if (x == box[0] or x == box[2]) and (y == box[1] or y == box[3]):
          print 'corner', x, y, distance, r
          count += tri(r)
        elif x == box[0] or x == box[2] or y == box[1] or y == box[3]:
          print 'edge', x, y, distance, r
          count += r
        else:
          count += 1
  return count


if __name__ == '__main__':
  input = get_input()
  print part1(input)
  print part2(input)
