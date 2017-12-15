import re


def get_input():
    with open('day5.txt') as fp:
        input = fp.read().strip()
    
    return input.split('\n')
# end get_input

def nice(line):
    return re.search(r'([aeiou].*){3}',line) and re.search(r'([a-z])\1', line) and not re.search(r'ab|cd|pq|xy', line)
# end nice

def part1(lines):
    return len([line for line in lines if nice(line)])
# end part1

def nice2(line):
    return re.search(r'([a-z][a-z]).*\1', line) and re.search(r'([a-z]).\1', line)
# end nice2

def part2(lines):
    return len([line for line in lines if nice2(line)])
# end part2

if __name__ == '__main__':
    lines = get_input()
    print part1(lines)
    print part2(lines)

