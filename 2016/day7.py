import re


def get_input():
    with open('day7.txt') as fp:
        input = fp.read().strip()
    
    return input.split('\n')
# end get_input

def part1(lines):
    count = 0
    for line in lines:
        if re.search(r'([a-z])(?!\1)([a-z])\2\1', line) and not re.search(r'\[[a-z]*([a-z])(?!\1)([a-z])\2\1[a-z]*\]', line):
            count += 1
    return count
# end part1

def part2(lines):
    count = 0
    for line in lines:
        if re.search(r'([a-z])(?!\1)([a-z])\1[a-z]*(\[[a-z]*\][a-z]*|\][a-z]*\[[a-z]*)*[[\]][a-z]*\2\1\2', line):
            count += 1
    return count
# end part2

if __name__ == '__main__':
    lines = get_input()
    print part1(lines)
    print part2(lines)

