import re


def get_input():
    with open('day1.txt') as fp:
        input = fp.read().strip()
    return re.split(r',\s*', input)
# end get_input

def part1(dirs):
    x = 0
    y = 0
    dx = 0
    dy = 1
    for dir in dirs:
        if dir[0] == 'L':
            dx, dy = -dy, dx
        else:
            dx, dy = dy, -dx
        blocks = int(dir[1:])
        x += dx*blocks
        y += dy*blocks
    return abs(x)+abs(y)
# end part1

def part2(dirs):
    x = 0
    y = 0
    dx = 0
    dy = 1
    past = [(0,0)]
    for dir in dirs:
        if dir[0] == 'L':
            dx, dy = -dy, dx
        else:
            dx, dy = dy, -dx
        blocks = int(dir[1:])
        for i in xrange(blocks):
            x += dx
            y += dy
            loc = (x,y)
            if loc in past:
                return abs(x)+abs(y)
            else:
                past.append(loc)
# end part2

if __name__ == '__main__':
    dirs = get_input()
    print part1(dirs)
    print part2(dirs)

