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

  return [re.search(r'Step ([A-Z]) must be finished before step ([A-Z]) can begin\.', line).groups() for line in input.split('\n')]


def part1(input):
  alphabet = set()
  requirements = {}
  enables = {}
  for pre, post in input:
    alphabet.add(pre)
    alphabet.add(post)
    requirements.setdefault(post, set()).add(pre)
    enables.setdefault(pre, set()).add(post)
  ready = alphabet - set(requirements.keys())
  done = ''
  while ready:
    next = min(ready)
    ready.discard(next)
    done += next
    for check in enables.get(next, set()):
      if check in done or check in ready:
        continue
      if all(pre in done for pre in requirements.get(check, set())):
        ready.add(check)
  return done

def part2(input):
  num_workers = 5
  base_time = 60

  alphabet = set()
  requirements = {}
  enables = {}
  for pre, post in input:
    alphabet.add(pre)
    alphabet.add(post)
    requirements.setdefault(post, set()).add(pre)
    enables.setdefault(pre, set()).add(post)
  ready = alphabet - set(requirements.keys())
  enqueued = set()
  done = ''
  workers = [{'step': None, 'remaining': 0} for i in xrange(num_workers)]
  t = 0
  while len(done) < len(alphabet):
    for worker in workers:
      if worker['remaining']:
        worker['remaining'] -= 1
        if not worker['remaining']:
          done += worker['step']
          for check in enables.get(worker['step'], set()):
            if check in enqueued or check in ready:
              continue
            if all(pre in done for pre in requirements.get(check, set())):
              ready.add(check)
          worker['step'] = None
      if not worker['remaining'] and ready:
        worker['step'] = min(ready)
        ready.discard(worker['step'])
        enqueued.add(worker['step'])
        worker['remaining'] = base_time + ord(worker['step']) - ord('A') + 1
    ## print t, [worker['step'] or '.' for worker in workers], done
    ## print t, workers, done
    ## import msvcrt
    ## if msvcrt.getch() == 27:
      ## sys.exit()
    t += 1
  return t - 1


if __name__ == '__main__':
  input = get_input()
  print part1(input)
  print part2(input)
