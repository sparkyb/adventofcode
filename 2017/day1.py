import re


def get_input():
    with open('day1.txt') as fp:
        return fp.read().strip()
# end get_input

def part1(input):
    sum = 0
    for i in xrange(len(input)):
        if input[i] == input[(i+1)%len(input)]:
            sum += int(input[i])
    return sum
# end part1

def part2(input):
    sum = 0
    for i in xrange(len(input)):
        if input[i] == input[(i+len(input)/2)%len(input)]:
            sum += int(input[i])
    return sum
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

