import os.path
import re
import math
from collections import defaultdict
from itertools import permutations,combinations_with_replacement


def get_input(filename=None):
    if not filename:
        filename = os.path.splitext(os.path.basename(__file__))[0]+'.txt'
    with open(filename) as fp:
        input = fp.read().strip()

    return dict((groups[0],dict((k, int(v)) for k,v in zip(groups[1::2],groups[2::2]))) for groups in (re.search(r'^(\w+): (capacity) ([0-9-]+), (durability) ([0-9-]+), (flavor) ([0-9-]+), (texture) ([0-9-]+), (calories) ([0-9-]+)$', line).groups() for line in input.split('\n')))
# end get_input

def part1(ingredients):
    max_score = 0
    for parts in combinations_with_replacement(ingredients.values(),100):
        score = defaultdict(int)
        for ingredient in parts:
            for k,v in ingredient.items():
                score[k]+=v
        score = reduce((lambda a,b:a*b),(1 if k=='calories' else max(v,0) for k,v in score.items()),1)
        if score > max_score:
            max_score = score
    return max_score
# end part1

def part2(ingredients):
    max_score = 0
    for parts in combinations_with_replacement(ingredients.values(),100):
        score = defaultdict(int)
        for ingredient in parts:
            for k,v in ingredient.items():
                score[k]+=v
            if score['calories'] > 500:
                break
        if score['calories'] != 500:
            continue
        score = reduce((lambda a,b:a*b),(1 if k=='calories' else max(v,0) for k,v in score.items()),1)
        if score > max_score:
            max_score = score
    return max_score
# end part2

if __name__ == '__main__':
    ingredients = get_input()
    print part1(ingredients)
    print part2(ingredients)

