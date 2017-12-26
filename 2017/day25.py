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

    return input.split('\n')
# end get_input

def part1(input):
    states = {}
    states['A'] = [{'write':1,'move':1,'next':'B'},
                   {'write':0,'move':-1,'next':'B'}]
    states['B'] = [{'write':0,'move':1,'next':'C'},
                   {'write':1,'move':-1,'next':'B'}]
    states['C'] = [{'write':1,'move':1,'next':'D'},
                   {'write':0,'move':-1,'next':'A'}]
    states['D'] = [{'write':1,'move':-1,'next':'E'},
                   {'write':1,'move':-1,'next':'F'}]
    states['E'] = [{'write':1,'move':-1,'next':'A'},
                   {'write':0,'move':-1,'next':'D'}]
    states['F'] = [{'write':1,'move':1,'next':'A'},
                   {'write':1,'move':-1,'next':'E'}]
    state = 'A'
    cursor = 0
    tape = defaultdict(int)
    for i in xrange(12629077):
        s = states[state][tape[cursor]]
        tape[cursor] = s['write']
        cursor += s['move']
        state = s['next']
    return sum(tape.values())
# end part1

def part2(input):
    return None
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

