import collections
from collections import defaultdict
import enum
import functools
import itertools
import math
import msvcrt
import operator
import os.path
import re
import sys

#import numpy as np


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip('\n')

  rules = {}
  messages = []

  in_rules = True

  for line in input.split('\n'):
    if in_rules:
      if not line:
        in_rules = False
        continue
      match = re.search(
          r'^(\d+): (?:\"(\w)\"|(\d+(?: \d+)*(?: \| \d+(?: \d+)*)*))$',
          line)
      rule_num = int(match.group(1))
      if match.group(2):
        rules[rule_num] = match.group(2)
      else:
        rules[rule_num] = [list(map(int, re.findall(r'\d+', option)))
                           for option in match.group(3).split('|')]
    else:
      messages.append(line)
  return rules, messages


def match_rules(rules, rule_nums, message):
  if not rule_nums:
    return not message
  rule_num, *rule_nums = rule_nums
  rule = rules[rule_num]
  if isinstance(rule, str):
    return (message.startswith(rule) and
            match_rules(rules, rule_nums,message[len(rule):]))
  else:
    return any(match_rules(rules, option + rule_nums, message)
               for option in rule)


def part1(input):
  rules, messages = input
  return sum(match_rules(rules, [0], message) for message in messages)


def part2(input):
  rules, messages = input
  rules[8] = [[42], [42, 8]]
  rules[11] = [[42, 31], [42, 11, 31]]
  return sum(match_rules(rules, [0], message) for message in messages)


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(part1(input))
  print(part2(input))
