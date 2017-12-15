import re


def get_input():
    with open('day3.txt') as fp:
        input = fp.read().strip()
    return [[int(val) for val in re.split(r'\s+', line.strip())] for line in input.split('\n')]
# end get_input

def part1(rows):
    sum = 0
    for row in rows:
        row = sorted(row)
        if row[0]+row[1]>row[2]:
            sum += 1
    return sum
# end part1

def part2(rows):
    return part1(sum([zip(*rows) for rows in zip(rows[0::3], rows[1::3], rows[2::3])], []))
# end part2

if __name__ == '__main__':
    rows = get_input()
    print part1(rows)
    print part2(rows)

