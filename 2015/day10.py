import re
import itertools


def get_input():
    with open('day10.txt') as fp:
        input = fp.read().strip()

    return input
# end get_input

def lookandsay(line):
    out = ""
    i = 0
    while i < len(line):
        j = i + 1
        while j < len(line) and line[j] == line[i]:
            j += 1
        out += str(j-i)+line[i]
        i = j
    return out
# end lookandsay

def part1(line):
    for i in xrange(40):
        line = lookandsay(line)
    return len(line)
# end part1

def part2(line):
    for i in xrange(50):
        line = lookandsay(line)
    return len(line)
# end part2

if __name__ == '__main__':
    line = get_input()
    print part1(line)
    print part2(line)

