import re


def get_input():
    with open('day8.txt') as fp:
        input = fp.read().strip()
    
    return [re.search(r'^(?:rect (\d+)x(\d+)|rotate (column x|row y)=(\d+) by (\d+))$', line).groups() for line in input.split('\n')]
# end get_input

def calcgrid(lines):
    grid = ['.'*50 for i in xrange(6)]
    for w,h,a,i,d in lines:
        if not a:
            w = int(w)
            h = int(h)
            for r in xrange(h):
                grid[r] = '#'*w + grid[r][w:]
        else:
            i = int(i)
            d = int(d)
            if a.startswith('row'):
                grid[i] = grid[i][-d:] + grid[i][:-d]
            else:
                cols = [''.join(col) for col in zip(*grid)]
                cols[i] = cols[i][-d:] + cols[i][:-d]
                grid = [''.join(row) for row in zip(*cols)]
    return grid
# end calcgrid

def part1(lines):
    grid = calcgrid(lines)
    return ''.join(grid).count('#')
# end part1

def part2(lines):
    grid = calcgrid(lines)
    for line in grid:
        print line
# end part2

if __name__ == '__main__':
    lines = get_input()
    print part1(lines)
    print part2(lines)

