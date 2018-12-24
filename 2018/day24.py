import os.path
import re
import math
from collections import defaultdict
import itertools
import md5
import msvcrt
import sys


class Group(object):
  def __init__(self, type, id, n, hp, attack_damage, attack_type, initiative, weak, immune):
    self.type = type
    self.id = id
    self.n = n
    self.hp = hp
    self.attack_damage = attack_damage
    self.attack_type = attack_type
    self.initiative = initiative
    self.weak = weak
    self.immune = immune

  def clone(self, boost=0):
    return self.__class__(self.type, self.id, self.n, self.hp, self.attack_damage+boost, self.attack_type, self.initiative, self.weak, self.immune)

  @property
  def power(self):
    return self.n * self.attack_damage

  def __nonzero__(self):
    return self.n > 0

  def damage(self, attacker):
    if attacker.attack_type in self.immune:
      return 0
    damage = attacker.power
    if attacker.attack_type in self.weak:
      damage *= 2
    return damage

  def attack(self, attacker):
    damage = self.damage(attacker)
    deaths = min(damage // self.hp, self.n)
    self.n -= deaths
    return deaths

def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0]+'.txt'
  with open(filename) as fp:
    input = fp.read().rstrip()

  groups = []
  type = None
  lines = input.split('\n')
  for line in lines:
    if re.search(r'^Immune System:$', line):
      type = 'immune'
    elif re.search(r'^Infection:$', line):
      type = 'infection'
    elif line:
      params = re.search(r'^(?P<n>\d+) units? each with (?P<hp>\d+) hit points? (?:\((?P<weakimmune>[^)]*)\) )?with an attack that does (?P<attack_damage>\d+) (?P<attack_type>\w+) damage at initiative (?P<initiative>\d+)$', line).groupdict()
      params['weak'] = []
      params['immune'] = []
      if params['weakimmune']:
        for statline in params['weakimmune'].split(';'):
          stat, attack_types = re.search(r'^\s*(weak|immune) to (.*?)\s*$', statline).groups()
          params[stat] = [attack_type.strip() for attack_type in attack_types.split(',')]
      groups.append(Group(type, len([group for group in groups if group.type == type]) + 1, int(params['n']), int(params['hp']), int(params['attack_damage']), params['attack_type'], int(params['initiative']), params['weak'], params['immune']))
  return groups

def print_groups(groups):
  print 'Immune System:'
  typegroups = sorted([group for group in groups if group.type == 'immune'], key=lambda g: g.id)
  for group in typegroups:
    print 'Group %d contains %d units' % (group.id, group.n)
  if not typegroups:
    print 'No groups remain.'
  print 'Infection:'
  typegroups = sorted([group for group in groups if group.type == 'infection'], key=lambda g: g.id)
  for group in typegroups:
    print 'Group %d contains %d units' % (group.id, group.n)
  if not typegroups:
    print 'No groups remain.'
  print

def round(groups):
  ## print_groups(groups)

  groups.sort(key=lambda g: (g.power, g.initiative), reverse=True)
  targets = {}
  for attacker in groups:
    possible_targets = [group for group in groups if group.type != attacker.type and group not in targets.values() and group.damage(attacker) > 0]
    if possible_targets:
      targets[attacker] = max(possible_targets, key=lambda g: (g.damage(attacker), g.power, g.initiative))
      ## print '%s group %d (%d, %d) would deal defending group %d %d damage' % (attacker.type.capitalize(), attacker.id, attacker.power, attacker.initiative, targets[attacker].id, targets[attacker].damage(attacker))
    ## else:
      ## print '%s group %d (%d, %d) cannot attack' % (attacker.type.capitalize(), attacker.id, attacker.power, attacker.initiative)
  ## print
  total_deaths = 0
  for attacker in sorted(targets.keys(), key=lambda g: g.initiative, reverse=True):
    deaths = targets[attacker].attack(attacker)
    ## print '%s group %d (%d) attacks defending group %d, killing %d units' % (attacker.type.capitalize(), attacker.id, attacker.initiative, targets[attacker].id, deaths)
    total_deaths += deaths
  ## print
  return [group for group in groups if group], total_deaths

def part1(groups):
  groups = [group.clone() for group in groups]
  while len(set(group.type for group in groups)) == 2:
    ## units = defaultdict(int)
    ## for group in groups:
      ## units[group.type] += group.n
    ## print dict(units)
    groups, _ = round(groups)
    ## if msvcrt.getch() == chr(27):
      ## sys.exit()
  ## print_groups(groups)
  return sum(group.n for group in groups)

def part2(orig_groups):
  boost = 1
  while True:
    ## print boost
    groups = [group.clone(boost if group.type == 'immune' else 0) for group in orig_groups]
    while len(set(group.type for group in groups)) == 2:
      groups, total_deaths = round(groups)
      if total_deaths == 0:
        ## print 'stalemate'
        break
    if len(set(group.type for group in groups)) == 1 and groups[0].type == 'immune':
      break
    boost += 1
  return sum(group.n for group in groups)


if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser(usage='%prog [options] [<input.txt>]')
  options, args = parser.parse_args()
  input = get_input(*args)
  print part1(input)
  print part2(input)
