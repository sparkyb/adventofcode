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

    return input
# end get_input

def parsegarbage(s, i):
    score = 0
    assert s[i] == '<'
    i += 1
    while s[i] != '>':
        if s[i] == '!':
            i += 2
        else:
            i += 1
            score += 1
    return i + 1, score

def parsegroup(s, i=0, depth=0):
    score = depth + 1
    gscore = 0
    assert s[i] == '{'
    i += 1
    while s[i] != '}':
        if s[i] == '{':
            i, score2, gscore2 = parsegroup(s, i, depth+1)
            score += score2
            gscore += gscore2
        else:
            assert s[i] == '<'
            i, gscore2 = parsegarbage(s, i)
            gscore += gscore2
        if s[i] == ',':
            i+=1
        else:
            assert s[i] == '}'
    return i+1, score, gscore

def parsegroups(s):
    depth = 0
    score = 0
    gscore = 0
    i = 0
    ingarbage = False
    assert s[0] == '{'
    while i < len(s):
        if ingarbage:
            if s[i] == '>':
                ingarbage = False
                i += 1
            elif s[i] == '!':
                i += 2
                continue
            else:
                i += 1
                gscore += 1
                continue
        elif s[i] == '{':
            depth += 1
            score += depth
            i += 1
            continue
        elif s[i] == '<':
            ingarbage = True
            i += 1
            continue
        elif s[i] == '}':
            depth -= 1
            i += 1
        else:
            raise ValueError('Unexpected character: %c @%d' % (s[i], i))
        if depth > 0:
            if s[i] == ',':
                i+=1
            else:
                assert s[i] == '}'
        else:
            assert i == len(s)
    assert depth == 0
    return score, gscore

def part1(input):
    ## i, score, gscore = parsegroup(input)
    ## assert i == len(input)
    score, gscore = parsegroups(input)
    return score
# end part1

def part2(input):
    ## i, score, gscore = parsegroup(input)
    ## assert i == len(input)
    score, gscore = parsegroups(input)
    return gscore
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

