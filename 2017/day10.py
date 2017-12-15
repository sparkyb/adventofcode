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

def part1(input):
    input = map(int,input.split(','))
    skip = 0
    nums = range(0,256)
    pos = 0
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
    return nums[0]*nums[1]
# end part1

def part2(input):
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
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

