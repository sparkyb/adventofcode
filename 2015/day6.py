import re


def get_input():
    with open('day6.txt') as fp:
        input = fp.read().strip()
    
    return [(op,(int(x),int(y)),(int(x2),int(y2))) for op,x,y,x2,y2 in (re.search(r'^(turn (?:on|off)|toggle) (\d+),(\d+) through (\d+),(\d+)$',line).groups() for line in input.split('\n'))]
# end get_input

def part1(ops):
    lights = [[False]*1000 for i in xrange(1000)]
    for op,(x1,y1),(x2,y2) in ops:
        x1,x2 = min(x1,x2),max(x1,x2)
        y1,y2 = min(y1,y2),max(y1,y2)
        for x in xrange(x1,x2+1):
            for y in xrange(y1,y2+1):
                if op == 'turn on':
                    lights[y][x] = True
                elif op == 'turn off':
                    lights[y][x] = False
                else:
                    lights[y][x] = not lights[y][x]
    return sum(sum(row) for row in lights)
# end part1

def part2(ops):
    lights = [[0]*1000 for i in xrange(1000)]
    for op,(x1,y1),(x2,y2) in ops:
        x1,x2 = min(x1,x2),max(x1,x2)
        y1,y2 = min(y1,y2),max(y1,y2)
        for x in xrange(x1,x2+1):
            for y in xrange(y1,y2+1):
                if op == 'turn on':
                    lights[y][x] += 1
                elif op == 'turn off':
                    lights[y][x] = max(lights[y][x]-1,0)
                else:
                    lights[y][x] += 2
    return sum(sum(row) for row in lights)
# end part2

if __name__ == '__main__':
    ops = get_input()
    print part1(ops)
    print part2(ops)

