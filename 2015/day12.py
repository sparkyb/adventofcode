import os.path
import re
import math
from collections import defaultdict
from itertools import permutations
import json


def get_input(filename=None):
    if not filename:
        filename = os.path.splitext(os.path.basename(__file__))[0]+'.txt'
    with open(filename) as fp:
        input = fp.read().strip()

    return json.loads(input)
# end get_input

def countnumbers(data):
    if isinstance(data, (list,tuple)):
        return sum(countnumbers(v) for v in data)
    elif isinstance(data, dict):
        return sum(countnumbers(v) for v in data.values())
    elif isinstance(data, (int,float)):
        return data
    else:
        return 0
# end countnumbers

def countnumbers2(data):
    if isinstance(data, (list,tuple)):
        return sum(countnumbers2(v) for v in data)
    elif isinstance(data, dict) and 'red' not in data.values():
        return sum(countnumbers2(v) for v in data.values())
    elif isinstance(data, (int,float)):
        return data
    else:
        return 0
# end countnumbers2

def part1(data):
    return countnumbers(data)
# end part1

def part2(data):
    return countnumbers2(data)
# end part2

if __name__ == '__main__':
    data = get_input()
    print part1(data)
    print part2(data)

