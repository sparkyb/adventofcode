import re


def get_input():
    with open('day2.txt') as fp:
        input = fp.read().strip()

    return [[int(val) for val in re.split(r'\s+', line)] for line in input.split('\n')]
# end get_input

def part1(rows):
    sum = 0
    for row in rows:
        row = sorted(row)
        sum += row[-1]-row[0]
    return sum
# end part1

def part2(rows):
    sum = 0
    for row in rows:
        row = sorted(row)
        found = False
        for a in reversed(row):
            for b in row:
                if a % b == 0:
                    sum += a/b
                    found = True
                    break
                elif b >= a/2:
                    break
            if found:
                break
    return sum
# end part2

if __name__ == '__main__':
    rows = get_input()
    print part1(rows)
    print part2(rows)

