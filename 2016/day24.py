import re
import itertools

class Maze(object):
    def __init__(self, rows):
        self.rows = rows
        self.numbers = {}
        for y,row in enumerate(self.rows):
            for x,c in enumerate(row):
                if c.isdigit():
                    self.numbers[int(c)] = (x,y)
    # end __init__

    def wall(self, x, y):
        return self.rows[y][x] == '#'
    # end wall

# end class Maze

def get_input():
    with open('day24.txt') as fp:
        input = fp.read().strip()
    
    return Maze(input.split('\n'))
# end get_input

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

def bfs(start, goal_func, neighbors_func):
    explored = set()
    frontier = [start]
    g = {start: 0}
    while frontier:
        current = frontier.pop(0)
        explored.add(current)
        if goal_func(current):
            return current, g[current]
        for neighbor, distance in neighbors_func(current):
            if neighbor in explored:
                continue
            distance += g[current]
            if neighbor not in frontier:
                frontier.append(neighbor)
                g[neighbor] = distance
            elif distance < g[neighbor]:
                g[neighbor] = distance
        frontier.sort(key=lambda node: g[node])
# end bfs

def neighbors(maze):
    def wrapper(pos):
        for dx,dy in ((-1,0),(0, -1), (0, 1), (1, 0)):
            nx,ny = pos[0]+dx,pos[1]+dy
            if not maze.wall(nx, ny):
                yield (nx,ny), 1
    return wrapper
# end neighbors

def heuristic(goal):
    def wrapper(pos):
        return abs(pos[0]-goal[0])+abs(pos[1]-goal[1])
    return wrapper
# end heuristic

def goal(goal):
    def wrapper(pos):
        return pos == goal
    return wrapper
# end goal

def part1(maze):
    distances = {}
    numbers = list(maze.numbers.keys())
    numbers.sort()
    for i,a in enumerate(numbers):
        for b in numbers[i+1:]:
            start = maze.numbers[a]
            g = maze.numbers[b]
            distances[(a,b)] = astar(start,goal(g),neighbors(maze),heuristic(g))[1]
            print '%d -> %d = %d'%(a, b, distances[(a,b)])
    lowest_dist = None
    for order in itertools.permutations(numbers[1:]):
        dist = 0
        a = 0
        for b in order:
            dist += distances[tuple(sorted((a,b)))]
            a = b
            if lowest_dist is not None and dist >= lowest_dist:
                break
        if lowest_dist is None or dist < lowest_dist:
            lowest_dist = dist
    return lowest_dist
# end part1

def part2(maze):
    distances = {}
    numbers = list(maze.numbers.keys())
    numbers.sort()
    for i,a in enumerate(numbers):
        for b in numbers[i+1:]:
            start = maze.numbers[a]
            g = maze.numbers[b]
            distances[(a,b)] = astar(start,goal(g),neighbors(maze),heuristic(g))[1]
            print '%d -> %d = %d'%(a, b, distances[(a,b)])
    lowest_dist = None
    for order in itertools.permutations(numbers[1:]):
        dist = 0
        a = 0
        for b in order:
            dist += distances[tuple(sorted((a,b)))]
            a = b
            if lowest_dist is not None and dist >= lowest_dist:
                break
        else:
            dist += distances[tuple(sorted((a,0)))]
        if lowest_dist is None or dist < lowest_dist:
            lowest_dist = dist
    return lowest_dist
# end part2

if __name__ == '__main__':
    maze = get_input()
    print part1(maze)
    print part2(maze)
