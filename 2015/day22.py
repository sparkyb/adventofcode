import os.path
import re
import math
from collections import defaultdict
from itertools import permutations

class State(object):
    def __init__(self, boss_hp, boss_damage, difficulty=0, hp=50, mana=500, shield=0, poison=0, recharge=0):
        self.boss_hp = boss_hp
        self.boss_damage = boss_damage
        self.difficulty = difficulty
        self.hp = hp - difficulty
        self.mana = mana
        self.shield = shield
        self.poison = poison
        self.recharge = recharge
    # end __init__

    def __str__(self):
        return 'mana:%d hp:%s boss_hp:%s effects:%s'%(self.mana,self.hp,self.boss_hp,','.join('%s(%d)'%(effect,getattr(self,effect)) for effect in ('shield','poison','recharge') if getattr(self,effect)))
    # end __str__

    def won(self):
        return self.boss_hp <= 0
    # end won

    def lost(self):
        return self.hp <= 0
    # end lost

    def take_turn(self, cost, damage=0, heal=0, shield=0, poison=0, recharge=0):
        boss_hp = self.boss_hp
        hp = self.hp
        mana = self.mana

        assert mana >= cost
        mana -= cost

        # player's turn
        boss_hp = max(boss_hp - damage, 0)
        hp += heal

        if not shield:
            shield = self.shield
        else:
            assert not self.shield
        if not poison:
            poison = self.poison
        else:
            assert not self.poison
        if not recharge:
            recharge = self.recharge
        else:
            assert not self.recharge

        # before boss's turn
        if poison:
            boss_hp = max(boss_hp - 3, 0)
            poison -= 1
        if recharge:
            mana += 101
            recharge -= 1
        if shield:
            shield -= 1
        armor = 0
        if shield:
            armor = 7

        # boss's turn
        if boss_hp > 0:
            hp = max(hp - max(self.boss_damage - armor, 1) ,0)

        # before player's next turn
        if poison:
            boss_hp = max(boss_hp - 3, 0)
            poison -= 1
        if recharge:
            mana += 101
            recharge -= 1
        if shield:
            shield -= 1

        return State(boss_hp, self.boss_damage, self.difficulty, hp, mana, shield, poison, recharge)
    # end take_turn

    def neighbors(self):
        if self.mana >= 53:
            next = self.take_turn(53, damage=4)
            if not next.lost():
                yield next, 53
        if self.mana >= 73:
            next = self.take_turn(73, damage=2, heal=2)
            if not next.lost():
                yield next, 73
        if self.mana >= 113 and not self.shield:
            next = self.take_turn(113, shield=6)
            if not next.lost():
                yield next, 113
        if self.mana >= 173 and not self.poison:
            next = self.take_turn(173, poison=6)
            if not next.lost():
                yield next, 173
        if self.mana >= 229 and not self.recharge:
            next = self.take_turn(229, recharge=5)
            if not next.lost():
                yield next, 229
    # end neighbors

    def __hash__(self):
        return hash((self.boss_hp, self.boss_damage, self.hp, self.mana, self.shield, self.poison, self.recharge))
    # end __hash__

    def __eq__(self, other):
        return (self.boss_hp, self.boss_damage, self.hp, self.mana, self.shield, self.poison, self.recharge)==(other.boss_hp, other.boss_damage, other.hp, other.mana, other.shield, other.poison, other.recharge)
    # end __eq__

# end class State

def get_input(filename=None):
    if not filename:
        filename = os.path.splitext(os.path.basename(__file__))[0]+'.txt'
    with open(filename) as fp:
        input = fp.read().strip()

    return dict((k,int(v)) for k,v in (line.split(': ') for line in input.split('\n')))
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

def part1(boss):
    start = State(boss['Hit Points'], boss['Damage'])
    def goal(state):
        return state.won()
    def heuristic(state):
        return state.boss_hp * 279/26.
    return astar(start, goal, State.neighbors, heuristic)[1]
# end part1

def part2(boss):
    start = State(boss['Hit Points'], boss['Damage'], 1, 51)
    def goal(state):
        return state.won()
    def heuristic(state):
        return state.boss_hp * 279/26.
    return astar(start, goal, State.neighbors, heuristic)[1]
# end part2

if __name__ == '__main__':
    boss = get_input()
    print part1(boss)
    print part2(boss)

