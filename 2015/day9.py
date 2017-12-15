import re
import itertools


def get_input():
    with open('day9.txt') as fp:
        input = fp.read().strip()

    return dict(((min(city1,city2),max(city1,city2)),int(dist)) for city1,city2,dist in (re.search(r'^\s*(\w+)\s+to\s+(\w+)\s*=\s*(\d+)\s*$', line).groups() for line in input.split('\n')))
# end get_input

def part1(dists):
    cities = set()
    for city1,city2 in dists:
        cities.add(city1)
        cities.add(city2)
    min_dist = None
    for order in itertools.permutations(cities):
        dist = 0
        city1 = order[0]
        for city2 in order[1:]:
            dist += dists[(min(city1,city2),max(city1,city2))]
            if min_dist is not None and dist >= min_dist:
                break
            city1 = city2
        if min_dist is None or dist < min_dist:
            min_dist = dist
    return min_dist
# end part1

def part2(dists):
    cities = set()
    for city1,city2 in dists:
        cities.add(city1)
        cities.add(city2)
    max_dist = 0
    for order in itertools.permutations(cities):
        dist = 0
        city1 = order[0]
        for city2 in order[1:]:
            dist += dists[(min(city1,city2),max(city1,city2))]
            city1 = city2
        if dist > max_dist:
            max_dist = dist
    return max_dist
# end part2

if __name__ == '__main__':
    dists = get_input()
    print part1(dists)
    print part2(dists)

