import re

def get_input():
    with open('day22.txt') as fp:
        input = fp.read().strip()
    
    return [map(int,re.search(r'^\/dev\/grid\/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+\d+T\s+\d+%$', line).groups()) for line in input.split('\n')[2:]]
# end get_input

def from_nodes(nodes):
    map = dict(((x,y),used) for x,y,size,used in nodes if used < 100)
    width = max(x for x,y in map)+1
    height = max(y for x,y in map)+1
    walls = []
    hole = None
    for x in xrange(width):
        for y in xrange(height):
            used = map.get((x,y),100)
            if used == 0:
                assert not hole
                hole = (x,y)
            elif used >= 100:
                walls.append((x,y))
    assert hole
    return Grid(width,height,hole,frozenset(walls))
# end from_nodes

class Grid(object):
    def __init__(self, width, height, hole, walls=frozenset(), goal=None):
        self.width = width
        self.height = height
        self.walls = frozenset(walls)
        self.hole = tuple(hole)
        if not goal:
            goal = (self.width - 1,0)
        self.goal = goal
    # end __init__

    def __eq__(self, other):
        return self.hole == other.hole and self.goal == other.goal
    # end __eq__

    def __hash__(self):
        return hash((self.hole, self.goal))
    # end __hash__

    def move(self, new_hole):
        goal = self.goal
        if new_hole == self.goal:
            goal = self.hole
        assert (self.hole[0]==new_hole[0] and abs(self.hole[1]-new_hole[1])==1) or (self.hole[1]==new_hole[1] and abs(self.hole[0]-new_hole[0])==1)
        return Grid(self.width, self.height, new_hole, self.walls, goal)
    # end move

    def neighbors(self):
        for dx,dy in ((-1,0),(0, -1), (0, 1), (1, 0)):
            nx,ny = self.hole[0]+dx,self.hole[1]+dy
            if nx<0 or ny<0 or nx>=self.width or ny>=self.height or (nx,ny) in self.walls:
                continue
            yield self.move((nx,ny)), 1
    # end neighbors

    def heuristic(self):
        dist = abs(self.hole[0]-self.goal[0])+abs(self.hole[1]-self.goal[1])-1
        return dist+sum(self.goal)*5
    # end heuristic

    def is_goal(self):
        return self.goal == (0,0)
    # end is_goal

    def state(self, x, y):
        if (x,y) in self.walls:
            return '#'
        elif (x,y) == self.goal:
            return 'G'
        elif (x,y) == self.hole:
            return '_'
        elif (x,y) == (0,0):
            return '0'
        else:
            return '.'
    # end state

    def draw(self):
        for y in xrange(self.height):
            row = []
            for x in xrange(self.width):
                row.append(self.state(x,y))
            print ''.join(row)
    # end draw

# end class Grid

def astar_all(start, goal_func, neighbors_func, heuristic_func):
    explored = set()
    frontier = [start]
    g = {start: 0}
    h = {start: heuristic_func(start)}
    f = {start: h[start]}
    while frontier:
        current = frontier.pop(0)
        explored.add(current)
        if goal_func(current):
            yield current, g[current]
            continue
        for neighbor, distance in neighbors_func(current):
            if neighbor in explored:
                continue
            distance += g[current]
            if neighbor not in frontier:
                frontier.append(neighbor)
                g[neighbor] = distance
                h[neighbor] = heuristic_func(neighbor)
                f[neighbor] = distance + h[neighbor]
            elif distance < g[neighbor]:
                g[neighbor] = distance
                f[neighbor] = distance + h[neighbor]
        frontier.sort(key=lambda node: (f[node],h[node]))
# end astar_all

def astar(start, goal_func, neighbors_func, heuristic_func):
    for result in astar_all(start, goal_func, neighbors_func, heuristic_func):
        return result
    return None
# end astar

def part1(nodes):
    viable = []
    for x,y,size,used in nodes:
        if not used:
            continue
        for x2,y2,size2,used2 in nodes:
            if (x,y) != (x2,y2) and used+used2<=size2:
                viable.append(((x,y),(x2,y2)))
    return len(viable)
# end part1

def part2(nodes):
    grid = from_nodes(nodes)
    def goal(grid):
        ## grid.draw()
        ## print grid.heuristic()
        ## raw_input()
        return grid.is_goal()
    return astar(grid,goal,Grid.neighbors,Grid.heuristic)[1]
# end part2

if __name__ == '__main__':
    nodes = get_input()
    print part1(nodes)
    print part2(nodes)
