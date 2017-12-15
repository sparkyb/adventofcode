import re


def get_input():
    with open('day6.txt') as fp:
        input = fp.read().strip()
    
    return input.split('\n')
# end get_input

def part1(rows):
    cols = zip(*rows)
    return ''.join(sorted((-col.count(c),c) for c in set(col))[0][1] for col in cols)
# end part1

def part2(rows):
    cols = zip(*rows)
    return ''.join(sorted((-col.count(c),c) for c in set(col))[-1][1] for col in cols)
# end part2

if __name__ == '__main__':
    rows = get_input()
    print part1(rows)
    print part2(rows)

