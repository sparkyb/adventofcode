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

    return dict((name,(int(weight),children and re.split(r',\s*', children) or [])) for name, weight, children in (re.search(r'^(\w+)\s*\((\d+)\)(?:\s*->\s*((?:\w+,\s*)*\w+))?$', line).groups() for line in input.split('\n')))
# end get_input

def part1(input):
    for prog in input:
        if any(prog in children for weight,children in input.values()):
            continue
        return prog
# end part1

def weight(input, name):
    return input[name][0]+sum(childweights(input,name).values())

def childweights(input, name):
    return dict((child,weight(input, child)) for child in input[name][1])

def diffkey(weights):
    weights = list(weights.items())
    n1, w1 = weights[0]
    n2, w2 = weights[1]
    for n,w in weights[2:]:
        if w != w1:
            if w1 == w2:
                return n, w1-w
            else:
                return n1, w-w1
        elif w != w2:
            return n2, w-w2
    return None
            

def part2(input):
    base = part1(input), None
    while base:
        prev = base
        cw = childweights(input, base[0])
        print base, cw
        base = diffkey(cw)
    return input[prev[0]][0]+prev[1]
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

