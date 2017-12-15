import re


def get_input():
    with open('day1.txt') as fp:
        input = fp.read().strip()
    return input
# end get_input

def part1(input):
    return input.count('(')-input.count(')')
# end part1

def part2(input):
    floor = 0
    for i,d in enumerate(input):
        floor += 1 if d=='(' else -1
        if floor < 0:
            return i + 1
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

