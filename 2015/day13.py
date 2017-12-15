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

    return dict(((a,b),int(amount)*(1 if dir=='gain' else -1)) for a,dir,amount,b in (re.search(r'^(\w+) would (lose|gain) (\d+) happiness units? by sitting next to (\w+)\.$', line).groups() for line in input.split('\n')))
# end get_input

def part1(rules):
    people = set()
    for a,b in rules:
        people.add(a)
        people.add(b)
    max_happiness = None
    for order in permutations(people):
        happiness = 0
        a = order[-1]
        for b in order:
            happiness += rules.get((a,b),0)+rules.get((b,a),0)
            a = b
        if max_happiness is None or happiness > max_happiness:
            max_happiness = happiness
    return max_happiness
# end part1

def part2(rules):
    people = set(['Me'])
    for a,b in rules:
        people.add(a)
        people.add(b)
    max_happiness = None
    for order in permutations(people):
        happiness = 0
        a = order[-1]
        for b in order:
            happiness += rules.get((a,b),0)+rules.get((b,a),0)
            a = b
        if max_happiness is None or happiness > max_happiness:
            max_happiness = happiness
    return max_happiness
# end part2

if __name__ == '__main__':
    rules = get_input()
    print part1(rules)
    print part2(rules)

