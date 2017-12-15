import os.path
import re
import math
from collections import defaultdict
from itertools import permutations


def get_input(filename=None):
    if not filename:
        filename = os.path.splitext(os.path.basename(__file__))[0]+'.txt'
    with open(filename) as fp:
        input = fp.read().strip()

    return dict((name, (int(speed), int(on), int(off))) for name, speed, on, off in (re.search(r'^(\w+) can fly (\d+) km/s for (\d+) seconds?, but then must rest for (\d+) seconds?\.$', line).groups() for line in input.split('\n')))
# end get_input

def fly(speed, on, off, duration):
    dist = 0
    while duration:
        dist += speed * min(on, duration)
        duration -= min(on, duration)
        duration -= min(off, duration)
    return dist
# end fly

def part1(reindeer):
    return max(fly(speed,on,off,2503) for speed,on,off in reindeer.values())
# end part1

def part2(reindeer):
    scores = defaultdict(int)
    for i in xrange(1,2504):
        max_distance = 0
        leading = []
        for name,(speed,on,off) in reindeer.items():
            dist = fly(speed,on,off,i)
            if dist > max_distance:
                max_distance = dist
                leading = [name]
            elif dist == max_distance:
                leading.append(name)
        for name in leading:
            scores[name]+=1
    return max(scores.values())
# end part2

if __name__ == '__main__':
    reindeer = get_input()
    print part1(reindeer)
    print part2(reindeer)

