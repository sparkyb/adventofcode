import re


def get_input():
    with open('day5.txt') as fp:
        input = fp.read().strip()

    return [int(line) for line in input.split('\n')]
# end get_input

def part1(lines):
    lines = list(lines)
    count = 0
    i = 0
    while i >=0 and i < len(lines):
        j=i+lines[i]
        lines[i]+=1
        i=j
        count += 1
    return count
# end part1

def part2(lines):
    lines = list(lines)
    count = 0
    i = 0
    while i >=0 and i < len(lines):
        j=i+lines[i]
        lines[i]+=-1 if lines[i]>=3 else 1
        i=j
        count += 1
    return count
# end part2

if __name__ == '__main__':
    lines = get_input()
    print part1(lines)
    print part2(lines)

