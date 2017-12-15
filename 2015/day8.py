import re
from collections import defaultdict


def get_input():
    with open('day8.txt') as fp:
        input = fp.read().strip()

    return input.split('\n')
# end get_input

def encode(line):
    out = ''
    for c in line:
        if c in '\\"':
            out += '\\' + c
        else:
            out += c
    return '"%s"'%out

def part1(lines):
    code = sum(len(line) for line in lines)
    memory = sum(len(eval(line)) for line in lines)
    return code-memory
# end part1

def part2(lines):
    code = sum(len(line) for line in lines)
    encoded = sum(len(encode(line)) for line in lines)
    return encoded-code
# end part2

if __name__ == '__main__':
    lines = get_input()
    print part1(lines)
    print part2(lines)

