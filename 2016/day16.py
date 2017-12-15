import re


def get_input():
    with open('day16.txt') as fp:
        input = fp.read().strip()
    
    return input
# end get_input

def pad(data, length):
    while len(data) < length:
        data = data + '0' + ''.join('1' if c=='0' else '0' for c in reversed(data))
    return data[:length]
# end pad

def checksum(data):
    while len(data) % 2 == 0:
        data = ''.join('1' if a==b else '0' for a,b in zip(data[0::2],data[1::2]))
    return data
# end checksum

def part1(input):
    return checksum(pad(input,272))
# end part1

def part2(input):
    return checksum(pad(input,35651584))
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

