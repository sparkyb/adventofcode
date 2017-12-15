import re


def get_input():
    with open('day18.txt') as fp:
        input = fp.read().strip()
    
    return [c=='^' for c in input]
# end get_input

def get_rows(first_row, n):
    row = first_row
    for r in xrange(n):
        yield row
        row = [(row[i-1] if i else False)!=(row[i+1] if i<len(row)-1 else False) for i in xrange(len(row))]
# end get_rows

def part1(first_row):
    safe = 0
    for row in get_rows(first_row, 40):
        #print ''.join('^' if t else '.' for t in row),sum(row),len(row)-sum(row)
        safe += len(row)-sum(row)
    return safe
# end part1

def part2(first_row):
    safe = 0
    for row in get_rows(first_row, 400000):
        #print ''.join('^' if t else '.' for t in row),sum(row),len(row)-sum(row)
        safe += len(row)-sum(row)
    return safe
# end part2

if __name__ == '__main__':
    first_row = get_input()
    print part1(first_row)
    print part2(first_row)

