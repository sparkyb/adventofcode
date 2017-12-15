import re


def get_input():
    with open('day3.txt') as fp:
        input = fp.read().strip()
    return input
# end get_input

def part1(input):
    x = 0
    y = 0
    houses = set([(x,y)])
    for dir in input:
        if dir == '^':
            y -= 1
        elif dir == 'v':
            y += 1
        elif dir == '<':
            x -= 1
        elif dir == '>':
            x += 1
        else:
            raise ValueError(dir)
        houses.add((x,y))
    return len(houses)
# end part1

def part2(input):
    x = 0
    y = 0
    houses = set([(x,y)])
    for dir in input[0::2]:
        if dir == '^':
            y -= 1
        elif dir == 'v':
            y += 1
        elif dir == '<':
            x -= 1
        elif dir == '>':
            x += 1
        else:
            raise ValueError(dir)
        houses.add((x,y))
    x = 0
    y = 0
    for dir in input[1::2]:
        if dir == '^':
            y -= 1
        elif dir == 'v':
            y += 1
        elif dir == '<':
            x -= 1
        elif dir == '>':
            x += 1
        else:
            raise ValueError(dir)
        houses.add((x,y))
    return len(houses)
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

