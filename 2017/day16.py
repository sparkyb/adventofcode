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

    return input.split(',')
# end get_input

def part1(input):
    line = [chr(ord('a')+i) for i in xrange(16)]
    for step in input:
        if step[0] == 's':
            size = int(step[1:])
            line = line[-size:]+line[:-size]
        elif step[0] == 'x':
            a,b = map(int, step[1:].split('/'))
            line[a],line[b] = line[b],line[a]
        elif step[0] == 'p':
            a,b = map(lambda x: line.index(x), step[1:].split('/'))
            line[a],line[b] = line[b],line[a]
    return ''.join(line)
# end part1

def part2(input):
    line = [chr(ord('a')+i) for i in xrange(16)]
    prev = [line]
    for i in xrange(1000000000):
        line = list(line)
        for step in input:
            if step[0] == 's':
                size = int(step[1:])
                line = line[-size:]+line[:-size]
            elif step[0] == 'x':
                a,b = map(int, step[1:].split('/'))
                line[a],line[b] = line[b],line[a]
            elif step[0] == 'p':
                a,b = map(lambda x: line.index(x), step[1:].split('/'))
                line[a],line[b] = line[b],line[a]
        if line in prev:
            prev_index = prev.index(line)
            return ''.join(prev[(1000000000-prev_index)%(i-prev_index+1)+prev_index])
        else:
            prev.append(line)
    return ''.join(line)
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

