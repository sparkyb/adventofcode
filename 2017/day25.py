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

    lines = input.split('\n')
    initial_state = re.search(r'^Begin in state (\w+)\.$', lines.pop(0)).group(1)
    iterations = int(re.search(r'^Perform a diagnostic checksum after (\d+) steps?\.$', lines.pop(0)).group(1))
    assert not lines.pop(0)
    states = {}
    while lines:
        state = re.search(r'^In state (\w+):$', lines.pop(0)).group(1)
        while lines and lines[0]:
            val = int(re.search('^\s*If the current value is ([01]):$', lines.pop(0)).group(1))
            write = int(re.search('^\s*- Write the value ([01])\.$', lines.pop(0)).group(1))
            move = re.search('^\s*- Move one slot to the (left|right)\.$', lines.pop(0)).group(1) == 'left' and -1 or 1
            next = re.search('^\s*- Continue with state (\w+)\.$', lines.pop(0)).group(1)
            states.setdefault(state, {})[val] = {'write': write, 'move': move, 'next': next}
        if lines:
            lines.pop(0)
    return initial_state, iterations, states
# end get_input

def part1(input):
    state, iterations, states = input
    cursor = 0
    tape = defaultdict(int)
    for i in xrange(iterations):
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

