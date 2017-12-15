import re


def get_input():
    with open('day4.txt') as fp:
        input = fp.read().strip()

    return [line.split() for line in input.split('\n')]
# end get_input

def part1(lines):
    return len([line for line in lines if len(line) == len(set(line))])
# end part1

def part2(lines):
    return len([line for line in lines if len(line) == len(set(frozenset(word) for word in line))])
# end part2

if __name__ == '__main__':
    lines = get_input()
    print part1(lines)
    print part2(lines)

