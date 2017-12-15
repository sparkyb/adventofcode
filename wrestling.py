import os.path
import re
import math
from collections import defaultdict
from itertools import permutations

def get_input(filename=None):
    if not filename:
        filename = os.path.splitext(os.path.basename(__file__))[0]+'.txt'
    with open(filename) as fp:
        input = fp.read().strip()

    return [re.search(r'\d+\s+([a-j]{2})\|([a-j]{2})\|([a-j]{2})\|([a-j]{2})\s+[a-j]{2}$', line).groups() for line in input.split('\n') if re.search(r'\d+\s+[a-j]{2}\|[a-j]{2}\|[a-j]{2}\|[a-j]{2}\s+[a-j]{2}$', line)]
# end get_input

def confirm(rounds):
  teams = set(chr(ord('a')+i) for i in xrange(10))
  buys = defaultdict(list)
  plays = defaultdict(dict)
  for i, round in enumerate(rounds):
    for t1,t2 in round:
      assert t2 not in plays[t1] and t1 not in plays[t2]
      plays[t1][t2] = i
      plays[t2][t1] = i
    playing = set(''.join(round))
    assert len(playing) == 8
    for t in teams - playing:
      buys[t].append(i)
  for t in teams:
    assert len(buys[t]) == 2
    assert any(i >= 4 for i in buys[t])
  assert 3 in buys['g']
  assert 3 in buys['h']
  assert 4 in buys['j']
  assert plays['c']['f'] == 0
  for t1, t2 in ['ae','bc','di','fj','gh']:
    assert t2 not in plays[t1] and t1 not in plays[t2]
  print 'Day 1:'
  for i, round in enumerate(rounds):
    print 'Round %d: %s, Buys: %s'%(i+1, ', '.join('%s vs. %s'%(t1.upper(),t2.upper()) for t1,t2 in round), ' and '.join(t.upper() for t in sorted(teams-set(''.join(round)))))
    if i == 3:
      print
      print 'Day 2:'

if __name__ == '__main__':
    confirm(get_input())
