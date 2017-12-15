import re
import math


def get_input():
    with open('day19.txt') as fp:
        input = fp.read().strip()
    
    return int(input)
# end get_input

def part1(n):
    return ((n-(1<<int(math.log(n)/math.log(2))))<<1)+1
# end part1

def part2(n):
    exp = int(math.log(n-1)/math.log(3))
    rem = n-pow(3,exp)
    if rem <= n/2:
        return rem
    else:
        return 3*rem-n
# end part2

"""
1 1

2 1
3 3

4 1
5 2
6 3
7 5
8 7
9 9

10 1
11 2
12 3
13 4
14 5
15 6
16 7
17 8
18 9
19 11
20 13
21 15
22 17
23 19
24 21
25 23
26 25
27 27

- - - - - - - - 9 - - - - - - - - -
- - - - - - - - - - 11 - - - - - - - -
- - - - - - - - - - - - 13 - - - - - - -
- - - - - - - - - - - - - - 15 - - - - - -
1 2 3 4 5 6 7 8 9 10 11 - - 14 15 16 17 18 19 20 21 22
1 2 3 4 5 6 7 8 9 10 11 - 13 - 15 16 17 18 19 20 21 22 23
1 2 3 4 5 6 7 8 9 10 11 12 - - 15 16 17 18 19 20 21 22 23 24
1 2 3 4 5 6 7 8 9 10 11 12 - 14 - 16 17 18 19 20 21 22 23 24 25
1 2 3 4 5 6 7 8 9 10 11 12 13 - - 16 17 18 19 20 21 22 23 24 25 26
1 2 3 4 5 6 7 8 9 10 11 12 13 - 15 - 17 18 19 20 21 22 23 24 25 26 27
"""

if __name__ == '__main__':
    n = get_input()
    print part1(n)
    print part2(n)

