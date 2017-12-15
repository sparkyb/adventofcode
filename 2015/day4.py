import re
import md5


def get_input():
    with open('day4.txt') as fp:
        input = fp.read().strip()
    
    return input
# end get_input

def part1(key):
    i = 0
    while True:
        hash = md5.md5(key+str(i)).hexdigest()
        if hash[:5] == '00000':
            return i
        i += 1
# end part1

def part2(key):
    i = 0
    while True:
        hash = md5.md5(key+str(i)).hexdigest()
        if hash[:6] == '000000':
            return i
        i += 1
# end part2

if __name__ == '__main__':
    key = get_input()
    print part1(key)
    print part2(key)

