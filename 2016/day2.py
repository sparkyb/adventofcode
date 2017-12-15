import re


def get_input():
    with open('day2.txt') as fp:
        input = fp.read().strip()
    return input.split('\n')
# end get_input

def adjacentkey(key, dir, keypad, width):
    index = keypad.index(key)
    if dir == 'U' and index >= width:
        index -= width
    elif dir == 'D' and index + width < len(keypad):
        index += width
    elif dir == 'L' and index % width > 0:
        index -= 1
    elif dir == 'R' and index % width < width - 1:
        index += 1
    if keypad[index] and keypad[index] != ' ':
        return keypad[index]
    return key
# end adjacentkey

def findcode(dirs, keypad, width):
    key = '5'
    code = ''
    for row in dirs:
        for dir in row:
            key = adjacentkey(key, dir, keypad, width)
        code += key
    return code
# end findcode

def part1(dirs):
    return findcode(dirs, '123456789', 3)
# end part1

def part2(dirs):
    return findcode(dirs, '  1   234 56789 ABC   D  ', 5)
# end part2

if __name__ == '__main__':
    dirs = get_input()
    print part1(dirs)
    print part2(dirs)

