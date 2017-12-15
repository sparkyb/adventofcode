import re
from collections import defaultdict


def get_input():
    with open('day3.txt') as fp:
        input = fp.read().strip()

    return int(input)
# end get_input

def get_coord(n):
    if n == 1:
        return (0,0)
    ring = 0
    while pow(ring*2+1,2)<n:
        ring += 1
    n -= pow((ring-1)*2+1,2)+1
    side,n = divmod(n,2*ring)
    if side == 0:
        return (ring,n-ring+1)
    elif side == 1:
        return (ring-n-1,ring)
    elif side == 2:
        return (-ring,ring-n-1)
    elif side == 3:
        return (n-ring+1,-ring)
# end get_coord

def part1(n):
    return sum(abs(i) for i in get_coord(n))
# end part1

def part2(n):
    values = defaultdict(int)
    i = 0
    x = 0
    y = 0
    values[(x,y)] = 1
    while values[(x,y)] < n:
        i += 1
        x,y = get_coord(i)
        values[(x,y)] = sum(values[(x+dx,y+dy)] for dx in xrange(-1,2) for dy in xrange(-1,2))
    return values[(x,y)]
# end part2

if __name__ == '__main__':
    n = get_input()
    print part1(n)
    print part2(n)

