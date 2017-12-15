import os.path
import re
import math
from collections import defaultdict
import itertools
import md5


def get_input(filename=None):
    if not filename:
        filename = os.path.splitext(os.path.basename(__file__))[0]+'.txt'
    with open(filename) as fp:
        input = fp.read().strip()

    return input
# end get_input

def knot_hash(input):
    input = map(ord, input)
    input += [17, 31, 73, 47, 23]
    skip = 0
    nums = range(0,256)
    pos = 0
    for round in xrange(64):
        for l in input:
            sub = nums[pos:pos+l]
            while (len(sub) < l):
                sub += nums[:l-len(sub)]
            sub = list(reversed(sub))
            if pos+l > len(nums):
                wrap = pos+l-len(nums)
                nums[:wrap] = sub[-wrap:]
                nums[pos:] = sub[:-wrap]
            else:
                nums[pos:pos+l] = sub
            pos = (pos + l + skip) % len(nums)
            skip += 1
    dense = [reduce(lambda a,b: a^b, nums[i*16:i*16+16], 0) for i in xrange(16)]
    return ''.join('%02x'%x for x in dense)
# end knot_hash

def count_bits(n):
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count

def part1(input):
    count = 0
    for i in xrange(128):
        #print ''.join('{:04b}'.format(int(c,16)).replace('1','#').replace('0','.') for c in knot_hash(input+'-%d'%i))[:8]
        count += sum(count_bits(int(c,16)) for c in knot_hash(input+'-%d'%i))
    return count
# end part1

class UnionFind(object):
    def __init__(self):
        self.groups = {}
    # end __init__

    def find(self, key):
        return frozenset(self.groups.get(key, [key]))
    # end find

    def union(self, key1, key2):
        new_group = self.find(key1)|self.find(key2)
        for key in new_group:
            self.groups[key] = new_group
        return new_group
    # end union

# end class UnionFind

def part2(input):
    grid = []
    for i in xrange(128):
        grid.append(''.join('{:04b}'.format(int(c,16)) for c in knot_hash(input+'-%d'%i)))
    uf = UnionFind()
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c != '1':
                continue
            if x < len(row) - 1 and row[x+1]=='1':
                uf.union((x,y),(x+1,y))
            if y < len(grid) - 1 and grid[y+1][x]=='1':
                uf.union((x,y),(x,y+1))
    return len(set(uf.find((x,y)) for y, row in enumerate(grid) for x, c in enumerate(row) if c == '1'))
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

