import re


def get_input():
    with open('day20.txt') as fp:
        input = fp.read().strip()
    
    return [map(int,line.split('-')) for line in input.split('\n')]
# end get_input

def merge_ranges(ranges):
    out = []
    ranges = list(ranges)
    ranges.sort()
    while ranges:
        range = list(ranges.pop(0))
        while ranges and ranges[0][0] <= range[1] + 1:
            range[1] = max(range[1], ranges[0][1])
            ranges.pop(0)
        out.append(tuple(range))
    return out
# end merge_ranges

def allowed_ranges(blocked_ranges):
    out = []
    i = 0
    ranges = merge_ranges(blocked_ranges)
    while ranges:
        range = ranges.pop(0)
        if i < range[0]:
            out.append((i,range[0]-1))
        i = range[1] + 1
    max = 4294967295
    if i <= max:
        out.append((i, max))
    return out
# end allowed_ranges

def count_ranges(ranges):
    ranges = merge_ranges(ranges)
    return sum(range[1]-range[0]+1 for range in ranges)
# end count_ranges

def part1(ranges):
    return allowed_ranges(ranges)[0][0]
# end part1

def part2(ranges):
    return count_ranges(allowed_ranges(ranges))
# end part2

if __name__ == '__main__':
    ranges = get_input()
    print part1(ranges)
    print part2(ranges)

