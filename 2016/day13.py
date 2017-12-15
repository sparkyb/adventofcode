import re
from collections import defaultdict


def get_input():
    with open('day13.txt') as fp:
        input = fp.read().strip()
    
    return int(input)
# end get_input

def iswall(x,y,input,memo=None):
    if x < 0 or y < 0: return True
    if memo and (x,y) in memo:
        return memo[(x,y)]
    n = x*x+3*x+2*x*y+y+y*y+input
    parity = False
    while n:
        n &= n - 1
        parity = not parity
    if memo:
        memo[(x,y)] = parity
    return parity
# end iswall

def astar(start, goal, neighbors_func, heuristic_func):
    explored = set()
    frontier = [start]
    g = {start: 0}
    h = {start: heuristic_func(start, goal)}
    f = {start: h[start]}
    while frontier:
        current = frontier.pop(0)
        if current == goal:
            return g[current]
        explored.add(current)
        for neighbor, distance in neighbors_func(current):
            if neighbor in explored:
                continue
            distance += g[current]
            if neighbor not in frontier:
                frontier.append(neighbor)
                g[neighbor] = distance
                h[neighbor] = heuristic_func(neighbor, goal)
                f[neighbor] = distance + h[neighbor]
            elif distance < g[neighbor]:
                g[neighbor] = distance
                f[neighbor] = distance + h[neighbor]
        frontier.sort(key=lambda node: (f[node],h[node]))
    return None
# end astar

def heuristic(cur, goal):
    return abs(cur[0]-goal[0])+abs(cur[1]-goal[1])
# end heuristic

def neighbors(input, memo=None):
    def wrapped(cur):
        for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]:
            if not iswall(cur[0]+dx,cur[1]+dy,input,memo):
                yield (cur[0]+dx,cur[1]+dy),1
    return wrapped
# end neighbors

def part1(input):
    start = (1,1)
    goal = (31,39)
    return astar(start, goal, neighbors(input, {}), heuristic)
# end part1

def part2(input):
    start = (1,1)
    neighbors_func = neighbors(input, {})
    visited = set([start])
    distance = 0
    next_frontier = set([start])
    while next_frontier and distance < 50:
        frontier = next_frontier
        next_frontier = set()
        distance += 1
        for current in frontier:
            for neighbor, _ in neighbors_func(current):
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                next_frontier.add(neighbor)
    return len(visited)
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

