import re


def get_input():
    with open('day9.txt') as fp:
        input = fp.read().strip()
    
    return re.sub(r'\s+','',input)
# end get_input

def part1(line):
    count = 0
    m = re.search(r'^([A-Z]*)\((\d+)x(\d+)\)', line)
    while m:
        count += len(m.group(1))
        l = int(m.group(2))
        r = int(m.group(3))
        count += l*r
        line = line[m.end()+l:]
        m = re.search(r'^([A-Z]*)\((\d+)x(\d+)\)', line)
    count += len(line)
    return count
# end part1

def part2(line):
    count = 0
    m = re.search(r'^([A-Z]*)\((\d+)x(\d+)\)', line)
    while m:
        count += len(m.group(1))
        l = int(m.group(2))
        r = int(m.group(3))
        count += part2(line[m.end():m.end()+l])*r
        line = line[m.end()+l:]
        m = re.search(r'^([A-Z]*)\((\d+)x(\d+)\)', line)
    count += len(line)
    return count
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

