import os.path
import re
import math
import datetime
from collections import defaultdict
import itertools
import md5


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0]+'.txt'
  with open(filename) as fp:
    input = fp.read().strip()

  lines = sorted([(datetime.datetime(int(Y),int(M),int(D),int(h),int(m)),guard or e1 or e2) for Y,M,D,h,m,guard,e1,e2 in [re.search(r'^\[(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})\] (?:Guard #(\d+) begins shift|falls (asleep)|(wakes) up)\s*$', line).groups() for line in input.split('\n')]])
  guards = {}
  asleep = None
  guard = None
  for timestamp,event in lines:
    if event.isdigit():
      assert asleep is None
      guard = int(event)
    elif event == 'asleep':
      assert guard is not None and asleep is None
      assert timestamp.hour == 0
      asleep = timestamp
    elif event == 'wakes':
      assert guard is not None and asleep is not None
      assert asleep.date() == timestamp.date() and timestamp.hour == 0
      minutes = guards.setdefault(guard,{})
      for minute in range(asleep.minute, timestamp.minute):
        minutes[minute] = minutes.get(minute, 0) + 1
      asleep = None
    else:
      raise ValueError('Unknown event: %r' % event)
  return  guards


def findmax(seq, key):
  maxitem = None
  maxkey = None
  for item in seq:
    k = key(item)
    if maxitem is None or k > maxkey:
      maxitem = item
      maxkey = k
  return maxitem
    


def part1(guards):
  guard = findmax(guards.items(), key=lambda g: sum(g[1].values()))
  minute = findmax(guard[1].items(), key=lambda m: m[1])
  return guard[0]*minute[0]

def part2(guards):
  guard = findmax(guards.items(), key=lambda g: max(g[1].values()))
  minute = findmax(guard[1].items(), key=lambda m: m[1])
  return guard[0]*minute[0]


if __name__ == '__main__':
  input = get_input()
  print part1(input)
  print part2(input)
