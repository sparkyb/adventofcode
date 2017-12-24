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

    return [map(int,line.split('/')) for line in input.split('\n')]
# end get_input

def strength(path):
    return sum(part[0]+part[1] for part in path)
# end strength

def length(path):
    return (len(path), strength(path))
# end length

def bridge(parts, metric, input=0):
    best = []
    best_score = metric(best)
    for i,part in enumerate(parts):
        if (part[0] == input):
            path = [part]+bridge(parts[:i]+parts[i+1:], metric, part[1])
        elif (part[1] == input):
            path = [part]+bridge(parts[:i]+parts[i+1:], metric, part[0])
        else:
            continue
        score = metric(path)
        if score > best_score:
            best = path
            best_score = score
    return best
# end bridge

def part1(parts):
    return strength(bridge(parts, strength))
# end part1

def part2(parts):
    return strength(bridge(parts, length))
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

