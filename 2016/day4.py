import re


def get_input():
    with open('day4.txt') as fp:
        input = fp.read().strip()
    
    return [(name,int(sector),checksum) for name,sector,checksum in (re.search(r'^([a-z-]+)-(\d+)\[([a-z]{5})\]$',line).groups() for line in input.split('\n'))]
# end get_input

def filterdecoys(rows):
    return [(name,sector) for name,sector,checksum in rows if ''.join(c for n,c in sorted((-name.count(c),c) for c in set(name.replace('-',''))))[:5]==checksum]
# end filterdecoys

def part1(rows):
    return sum(sector for name,sector in filterdecoys(rows))
# end part1

def part2(rows):
    decrypted = [(''.join(' ' if c=='-' else chr((ord(c)-ord('a')+sector)%26+ord('a')) for c in name),sector) for name,sector in filterdecoys(rows)]
    for name, sector in decrypted:
        if 'northpole' in name:
            return sector
# end part2

if __name__ == '__main__':
    rows = get_input()
    print part1(rows)
    print part2(rows)

