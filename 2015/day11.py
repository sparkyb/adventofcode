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

    return input
# end get_input

def incpassword(password):
    password = [ord(c)-ord('a') for c in reversed(password)]
    i = 0
    done = False
    while i < len(password) and (not i or not password[i-1]):
        password[i] = (password[i]+1)%26
        i += 1
    return ''.join(chr(c+ord('a')) for c in reversed(password))
# end incpassword

def checkpassword(password):
    if re.search(r'[iol]', password):
        return False
    if not re.search(r'([a-z])\1.*(?!\1)([a-z])\2', password):
        return False
    for i,c in enumerate(password[:-2]):
        if ord(password[i+1])==ord(c)+1 and ord(password[i+2])==ord(c)+2:
            return True
    return False

def part1(password):
    while True:
        password = incpassword(password)
        if checkpassword(password):
            return password
# end part1

def part2(password):
    return part1(part1(password))
# end part2

if __name__ == '__main__':
    password = get_input()
    print part1(password)
    print part2(password)

