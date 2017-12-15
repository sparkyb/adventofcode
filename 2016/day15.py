import re


def get_input():
    with open('day15.txt') as fp:
        input = fp.read().strip()
    
    return [map(int,re.search(r'^Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+)\.$', line).groups()) for line in input.split('\n')]
# end get_input

def align(discs):
    t = 0
    while any((disc+t+start)%mod for disc,mod,start in discs):
        t += 1
    return t
# end align

def part1(discs):
    return align(discs)
# end part1

def part2(discs):
    return align(discs+[(len(discs)+1,11,0)])
# end part2

if __name__ == '__main__':
    discs = get_input()
    print part1(discs)
    print part2(discs)

