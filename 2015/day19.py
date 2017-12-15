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

    lines = input.split('\n')
    medicine = lines[-1]
    replacements = [re.search(r'^(\w+) => (\w+)$', line).groups() for line in lines[:-2]]
    return replacements, medicine
# end get_input

def astar_all(start, goal_func, neighbors_func, heuristic_func):
    explored = set()
    frontier = [start]
    came_from = {}
    g = {start: 0}
    h = {start: heuristic_func(start)}
    f = {start: h[start]}
    while frontier:
        current = frontier.pop(0)
        explored.add(current)
        if goal_func(current):
            path = []
            node = current
            while node:
                path.insert(0, node)
                node = came_from.get(node)
            yield path, g[current]
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
                came_from[neighbor] = current
            elif distance < g[neighbor]:
                g[neighbor] = distance
                f[neighbor] = distance + h[neighbor]
                came_from[neighbor] = current
        frontier.sort(key=lambda node: (f[node],h[node]))
# end astar_all

def astar(start, goal_func, neighbors_func, heuristic_func):
    for result in astar_all(start, goal_func, neighbors_func, heuristic_func):
        return result
    return None
# end astar

def neighbors(replacements, molecule):
    output = set()
    for f,t in replacements:
        i = molecule.find(f)
        while i >= 0:
            output.add(molecule[:i]+t+molecule[i+len(f):])
            i = molecule.find(f, i+len(f))
    return output
# end neighbors

def rneighbors(replacements, molecule):
    output = set()
    for f,t in replacements:
        i = molecule.find(t)
        while i >= 0:
            output.add(molecule[:i]+f+molecule[i+len(t):])
            i = molecule.find(t, i+len(t))
    return output
# end rneighbors

def part1(replacements, medicine):
    return len(neighbors(replacements, medicine))
# end part1

def part2(replacements, medicine):
    start = 'e'
    def neighbor_func(molecule):
        for result in rneighbors(replacements, molecule):
            if len(result)>len(medicine):
                continue
            yield result, 1
    def heuristic(molecule):
        return len(molecule)
    def goal(molecule):
        return molecule == 'e'

    return astar(medicine, goal, neighbor_func, heuristic)[1]
# end part2

if __name__ == '__main__':
    replacements, medicine = get_input()
    print part1(replacements, medicine)
    print part2(replacements, medicine)

