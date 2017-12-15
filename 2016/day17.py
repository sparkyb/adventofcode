import re
import md5
from collections import defaultdict


def get_input():
    with open('day17.txt') as fp:
        input = fp.read().strip()
    
    return input
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

def goal(state):
    return state[0] == 3 and state[1] == 3
# end goal

def heuristic(state):
    return 3-state[0]+3-state[1]
# end heuristic

def neighbors(input):
    def wrapper(state):
        x,y,path = state
        hash = md5.md5(input+path).hexdigest()
        for i,dir in enumerate('UDLR'):
            if hash[i] not in 'bcdef':
                continue
            dx = (i/2) and (i%2)*2-1 or 0
            dy = not (i/2) and (i%2)*2-1 or 0
            if x+dx < 0 or x+dx >= 4 or y+dy < 0 or y+dy >= 4:
                continue
            yield (x+dx,y+dy,path+dir),1
    return wrapper
# end neighbors

def part1(input):
    start = (0,0,'')
    return astar(start, goal, neighbors(input), heuristic)[0][-1]
# end part1

def part2(input):
    start = (0,0,'')
    return max(distance for state, distance in astar_all(start, goal, neighbors(input), heuristic))
# end part2

if __name__ == '__main__':
    input = get_input()
    print part1(input)
    print part2(input)

