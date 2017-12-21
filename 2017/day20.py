import os.path
import re
import math
from collections import defaultdict
import itertools
import md5

class Vector(tuple):
    def __add__(self, other):
        return Vector((a+b for a,b in zip(self, other)))
    def __sub__(self, other):
        return Vector((a-b for a,b in zip(self, other)))
    def __mul__(self, other):
        return Vector((a*other for a in self))
    def __div__(self, other):
        return Vector((a/other for a in self))
    def __floordiv__(self, other):
        return Vector((a//other for a in self))
    @property
    def length(self):
        return sum(abs(a) for a in self)
    def __eq__(self, other):
        return all(a==b for a,b in zip(self,other))
    def __ne__(self, other):
        return all(a!=b for a,b in zip(self,other))

class Particle(object):
    def __init__(self,p,v,a):
        self.p = Vector(p)
        self.v = Vector(v)
        self.a = Vector(a)
    def step(self,t=1):
        return Particle(self.p+self.v*t+self.a*t*(t+1)/2,self.v+self.a*t,self.a)
    def __add__(self, other):
        return Particle(self.p+other.p,self.v+other.v,self.a+other.a)
    def __sub__(self, other):
        return Particle(self.p-other.p,self.v-other.v,self.a-other.a)

def get_input(filename=None):
    if not filename:
        filename = os.path.splitext(os.path.basename(__file__))[0]+'.txt'
    with open(filename) as fp:
        input = fp.read().strip()

    return [Particle(**dict((l,Vector(map(int,v[1:-1].split(',')))) for l,v in (vec.split('=') for vec in line.split(', ')))) for line in input.split('\n')]
# end get_input

def part1(particles):
    min_accel = None
    mindex = None
    for i, particle in enumerate(particles):
        accel = particle.a.length
        if min_accel is None or accel < min_accel:
            min_accel = accel
            mindex = i
    return mindex
# end part1

def collide(particles):
    particles = list(particles)
    i = 0
    while i < len(particles):
        unique = True
        j = i + 1
        while j < len(particles):
            if particles[i].p == particles[j].p:
                unique = False
                particles = particles[:j]+particles[j+1:]
            else:
                j += 1
        if not unique:
            particles = particles[:i]+particles[i+1:]
        else:
            i += 1
    return particles
# end collide

def part2(particles):
    t = 0
    while True:
        print t, len(particles)
        particles = collide(particles)
        for i,particle1 in enumerate(particles):
            for particle2 in particles[i+1:]:
                diff = particle1-particle2
                if any(v*a<0 or p*v<0 for p,v,a in zip(diff.p,diff.v,diff.a)):
                    break
            else:
                continue
            break
        else:
            return len(particles)
        particles = [particle.step() for particle in particles]
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

