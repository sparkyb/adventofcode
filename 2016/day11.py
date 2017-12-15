import re
import msvcrt
import sys


class Floor(object):
    def __init__(self, microchips=(), generators=()):
        self.microchips = tuple(sorted(microchips))
        self.generators = tuple(sorted(generators))
    # end __init__

    def get_options(self):
        unpaired_generators = tuple(type for type in self.generators if type not in self.microchips)

        options = []
        
        if self.generators:
            if len(self.microchips) >= 2:
                options.append((self.microchips[:2],[]))
                if len(self.generators) == 2:
                    options.append(([],self.generators))
            if self.microchips:
                options.append((self.microchips[:1],self.microchips[:1]))
                options.append((self.microchips[:1],[]))
                if len(self.generators) == 1:
                    options.append(([],self.generators))
                elif len(self.generators) == 2 and len(self.microchips) == 1:
                    options.append(([],self.generators))
            for i, type in enumerate(unpaired_generators):
                options.append(([],[type]))
                for type2 in unpaired_generators[i+1:]:
                    options.append(([],[type,type2]))
        else:
            for i, type in enumerate(self.microchips):
                options.append(([type],[]))
                for type2 in self.microchips[i+1:]:
                    options.append(([type,type2],[]))
        
        options.sort(key=lambda option: len(option[0])+len(option[1]))
        return options
    # end get_options

    def can_drop(self, microchips, generators):
        for type in microchips:
            if type not in generators and type not in self.generators and (generators or self.generators):
                return False
        if not self.generators and generators:
            for type in self.microchips:
                if type not in generators:
                    return False
        return True
    # end can_drop
    
    def take(self, microchips, generators):
        return Floor([type for type in self.microchips if type not in microchips], [type for type in self.generators if type not in generators])
    # end take

    def drop(self, microchips, generators):
        return Floor(self.microchips+tuple(microchips), self.generators+tuple(generators))
    # end drop
    
    def __eq__(self, other):
        return self.microchips == other.microchips and self.generators == other.generators
    # end __eq__
    
    def __hash__(self):
        return hash((self.microchips, self.generators))
    # end __hash__

# end class Floor

class Situation(object):
    def __init__(self,floors,elevator=0):
        self.floors = tuple(floor if isinstance(floor,Floor) else Floor(*floor) for floor in floors)
        self.elevator = elevator
        assert self.elevator >=0 and self.elevator < len(self.floors)
        self.types = []
        types2 = []
        for floor in self.floors:
            for type in floor.microchips:
                assert type not in self.types
                self.types.append(type)
            for type in floor.generators:
                assert type not in types2
                types2.append(type)
        self.types.sort()
        types2.sort()
        assert self.types == types2
        self.types = tuple(self.types)

        items = 0
        steps = 0
        for i, floor in enumerate(self.floors[:-1]):
            items += len(floor.microchips)+len(floor.generators)
            if steps and i == self.elevator:
                items -= 1
            if items:
                if not steps and self.elevator > i:
                    items += 1
                    steps += self.elevator - i
                steps += 1 + 2*max(items-2,0)
        self.dist_to_target = steps
    # end __init__

    def get_options(self):
        options = []
        floor_options = self.floors[self.elevator].get_options()
        for dir in (1,-1):
            to_floor = self.elevator+dir
            if to_floor < 0 or to_floor >= len(self.floors):
                continue
            for microchips, generators in (floor_options if dir > 0 else reversed(floor_options)):
                if (not self.floors[to_floor].can_drop(microchips, generators)):
                    continue
                floors = list(self.floors)
                floors[self.elevator] = floors[self.elevator].take(microchips, generators)
                floors[to_floor] = floors[to_floor].drop(microchips, generators)
                options.append(Situation(floors,to_floor))
        return options
    # end get_options

    def draw(self):
        floor_digits = len(str(len(self.floors)))
        for i, floor in reversed(list(enumerate(self.floors))):
            line = [('F%%0%dd'%floor_digits)%(i+1),'E' if i==self.elevator else '.']
            for type in self.types:
                line.append('%sG'%type if type in floor.generators else '.'+' '*len(type))
                line.append('%sM'%type if type in floor.microchips else '.'+' '*len(type))
            print ' '.join(line)
    # end draw

    def __eq__(self, other):
        return self.floors == other.floors and self.elevator == other.elevator
    # end __eq__
    
    def __hash__(self):
        return hash((self.floors,self.elevator))
    # end __hash__

# end class Situation

def find_target(start):
    done = set()
    distance_to_target = {start:start.dist_to_target}
    distance_from_start = {start:0}
    frontier = [start]
    while frontier:
        situation = frontier.pop(0)
        if situation.dist_to_target == 0:
            return distance_to_target[situation]
        done.add(situation)
        dist = distance_from_start[situation]+1
        ## situation.draw()
        print distance_from_start[situation],distance_to_target[situation],len(frontier)
        ## if ord(msvcrt.getch()) == 27:
            ## sys.exit(1)
        for option in situation.get_options():
            if option in done:
                continue
            if option not in frontier:
                frontier.append(option)
                distance_from_start[option] = dist
                distance_to_target[option] = dist + option.dist_to_target
            elif dist < distance_from_start[option]:
                distance_from_start[option] = dist
                distance_to_target[option] = dist + option.dist_to_target
        frontier.sort(key=lambda option: (distance_to_target[option],-distance_from_start[option]))
    return None
# end find_target

def get_input():
    return Situation([(['H','L'],[]),([],['H']),([],['L']),([],[])])
    return Situation([(['T','R','C'],['Po','Pr','T','R','C']),(['Po','Pr'],[]),([],[]),([],[])])
# end get_input

def part1(start):
    return find_target(start)
# end part1

def part2(start):
    floors = list(start.floors)
    floors[0] = floors[0].drop(('E','D'), ('E','D'))
    start = Situation(floors)
    return find_target(start)
# end part2

if __name__ == '__main__':
    start = get_input()
    print part1(start)
    print part2(start)

