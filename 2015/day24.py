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

    return map(int, input.split('\n'))
# end get_input

def group_permutations(weights, total):
    if total == 0:
        yield frozenset(()), weights
    weights = list(weights)
    weights.sort(reverse=True)
    for i, w in enumerate(weights):
        if w > total: continue
        group = frozenset((w,))
        before = weights[:i]
        after = weights[i+1:]
        for g, r in group_permutations(after, total-w):
            yield group|g, before+r
# end group_permutations

def part1(weights):
    total = sum(weights)
    assert total % 3 == 0
    group_weight = total / 3
    min_num = len(weights)+1
    min_qe = None
    for first_group, remaining in group_permutations(weights, group_weight):
        if len(first_group) > min_num: continue
        qe = reduce(lambda a,b:a*b,first_group,1)
        if len(first_group) == min_num and qe >= min_qe: continue
        for g, r in group_permutations(remaining, group_weight):
            min_num = len(first_group)
            min_qe = qe
            print min_num, min_qe
            break
    return min_qe
# end part1

def part2(weights):
    total = sum(weights)
    assert total % 4 == 0
    group_weight = total / 4
    min_num = len(weights)+1
    min_qe = None
    for first_group, remaining in group_permutations(weights, group_weight):
        if len(first_group) > min_num: continue
        qe = reduce(lambda a,b:a*b,first_group,1)
        if len(first_group) == min_num and qe >= min_qe: continue
        for g, r in group_permutations(remaining, group_weight):
            for g2, r2 in group_permutations(r, group_weight):
                min_num = len(first_group)
                min_qe = qe
                print min_num, min_qe
                break
            else:
                continue
            break
    return min_qe
# end part2

if __name__ == '__main__':
    weights = get_input()
    print part1(weights)
    print part2(weights)

