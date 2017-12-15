import os.path
import re
import math
from collections import defaultdict
from itertools import permutations, combinations, product, chain


def get_input(filename=None):
    if not filename:
        filename = os.path.splitext(os.path.basename(__file__))[0]+'.txt'
    with open(filename) as fp:
        input = fp.read().strip()

    return dict((k,int(v)) for k,v in (line.split(': ') for line in input.split('\n')))
# end get_input

WEAPONS = [
    (8,4,0),
    (10,5,0),
    (25,6,0),
    (40,7,0),
    (74,8,0),
]

ARMOR = [
    (13, 0, 1),
    (31, 0, 2),
    (53, 0, 3),
    (75, 0, 4),
    (102, 0, 5),
]

RINGS = [
    (25, 1, 0),
    (50, 2, 0),
    (100, 3, 0),
    (20, 0, 1),
    (40, 0, 2),
    (80, 0, 3),
]

def part1(boss):
    min_cost = None
    for items in product(list(combinations(WEAPONS,1)),list(combinations(ARMOR,0))+list(combinations(ARMOR,1)),list(combinations(RINGS,0))+list(combinations(RINGS,1))+list(combinations(RINGS,2))):
        items = chain(*items)
        cost, damage, armor = map(sum, zip(*items))
        if (min_cost is None or cost < min_cost) and max(damage-boss['Armor'],1)>=max(boss['Damage']-armor,1):
            min_cost = cost
    return min_cost
# end part1

def part2(boss):
    max_cost = 0
    for items in product(list(combinations(WEAPONS,1)),list(combinations(ARMOR,0))+list(combinations(ARMOR,1)),list(combinations(RINGS,0))+list(combinations(RINGS,1))+list(combinations(RINGS,2))):
        items = chain(*items)
        cost, damage, armor = map(sum, zip(*items))
        if cost > max_cost and max(damage-boss['Armor'],1)<max(boss['Damage']-armor,1):
            max_cost = cost
    return max_cost
# end part2

if __name__ == '__main__':
    boss = get_input()
    print part1(boss)
    print part2(boss)

