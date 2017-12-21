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

    return dict(line.split(' => ') for line in input.split('\n'))
# end get_input

def splitimg(img):
    grid = img.split('/')
    imgs = []
    if len(grid) % 2 == 0:
        for y in xrange(len(grid) / 2):
            row = []
            for x in xrange(len(grid) / 2):
                row.append('/'.join(grid[y2][x*2:x*2+2] for y2 in xrange(y*2,y*2+2)))
            imgs.append(row)
    else:
        for y in xrange(len(grid) / 3):
            row = []
            for x in xrange(len(grid) / 3):
                row.append('/'.join(grid[y2][x*3:x*3+3] for y2 in xrange(y*3,y*3+3)))
            imgs.append(row)
    return imgs

def joinimgs(imgs):
    grid = []
    for row in imgs:
        grid.extend(''.join(row2) for row2 in zip(*(img.split('/') for img in row)))
    return '/'.join(grid)

def rotate(img):
    grid = img.split('/')
    return '/'.join(''.join(grid[-x-1][y] for x in xrange(len(grid))) for y in xrange(len(grid)))

def flipx(img):
    grid = img.split('/')
    return '/'.join(''.join(grid[y][-x-1] for x in xrange(len(grid))) for y in xrange(len(grid)))

def flipy(img):
    grid = img.split('/')
    return '/'.join(''.join(grid[-y-1][x] for x in xrange(len(grid))) for y in xrange(len(grid)))

def permutations(img):
    yield img
    yield rotate(img)
    flippedx = flipx(img)
    yield flippedx
    yield rotate(flippedx)
    flippedy = flipy(img)
    yield flippedy
    yield rotate(flippedy)
    flippedxy = flipy(flippedx)
    yield flippedxy
    yield rotate(flippedxy)

def replace(img, patterns):
    for pimg in permutations(img):
        if pimg in patterns:
            return patterns[pimg]
    raise ValueError('Couldn\'t find match for %s' % img)

def step(img, patterns):
    return joinimgs([replace(simg,patterns) for simg in row] for row in splitimg(img))

def part1(patterns):
    img = '.#./..#/###'
    for i in xrange(5):
        img = step(img, patterns)
    return img.count('#')
# end part1

def part2(patterns):
    img = '.#./..#/###'
    for i in xrange(18):
        img = step(img, patterns)
    return img.count('#')
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)
