import re


def get_input():
    with open('day2.txt') as fp:
        input = fp.read().strip()
    return [map(int,line.split('x')) for line in input.split('\n')]
# end get_input

def part1(boxes):
    sum = 0
    for box in boxes:
        box = sorted(box)
        sum += 3*box[0]*box[1]+2*box[0]*box[2]+2*box[1]*box[2]
    return sum
# end part1

def part2(boxes):
    sum = 0
    for box in boxes:
        box = sorted(box)
        sum += 2*box[0]+2*box[1]+box[0]*box[1]*box[2]
    return sum
# end part2

if __name__ == '__main__':
    boxes = get_input()
    print part1(boxes)
    print part2(boxes)

