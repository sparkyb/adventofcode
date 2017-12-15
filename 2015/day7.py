import re
from collections import defaultdict


def get_input():
    with open('day7.txt') as fp:
        input = fp.read().strip()

    return dict((output, op.split()) for op,output in (re.search(r'^((?:\w+|\d+) (?:AND|OR|LSHIFT|RSHIFT) (?:\w+|\d+)|NOT (?:\w+|\d+)|(?:\w+|\d+)) -> (\w+)$',line).groups() for line in input.split('\n')))
# end get_input

def run(ops, defaults=None):
    values = {}
    if defaults:
        values.update(defaults)
    stack = ['a']
    while stack:
        output = stack[-1]
        op = ops[output]
        if len(op) == 3:
            args = (op[0],op[2])
            op = op[1]
        elif len(op) == 2:
            args = (op[1],)
            op = op[0]
        else:
            args = (op[0],)
            op = None
        vals = []
        for arg in args:
            if arg.isdigit():
                vals.append(int(arg))
            elif arg in values:
                vals.append(values[arg])
            else:
                stack.append(arg)
        if len(vals) == len(args):
            stack.pop()
            if op is None:
                values[output] = vals[0]
            elif op == 'NOT':
                values[output] = ~vals[0]
            elif op == 'AND':
                values[output] = vals[0] & vals[1]
            elif op == 'OR':
                values[output] = vals[0] | vals[1]
            elif op == 'LSHIFT':
                values[output] = vals[0] << vals[1]
            elif op == 'RSHIFT':
                values[output] = vals[0] >> vals[1]
    return values['a']
# end run

def part1(ops):
    return run(ops)
# end part1

def part2(ops):
    return run(ops,{'b':part1(ops)})
# end part2

if __name__ == '__main__':
    ops = get_input()
    print part1(ops)
    print part2(ops)

