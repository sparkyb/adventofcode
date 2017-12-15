import re


def get_input():
    with open('day21.txt') as fp:
        input = fp.read().strip()
    
    return input.split('\n')
# end get_input

def scramble(password, ops):
    password = list(password)
    for line in ops:
        #print ''.join(password)
        m = re.search(r'^swap position (\d+) with position (\d+)$', line)
        if m:
            x, y = map(int, m.groups())
            password[x], password[y] = password[y], password[x]
            continue
        m = re.search(r'^swap letter ([a-z]) with letter ([a-z])$', line)
        if m:
            x, y = [password.index(l) for l in m.groups()]
            password[x], password[y] = password[y], password[x]
            continue
        m = re.search(r'^rotate (left|right) (\d+) steps?$', line)
        if m:
            x = int(m.group(2))
            if m.group(1) == 'left':
                x = -x
            x %= len(password)
            password = password[-x:]+password[:-x]
            continue
        m = re.search(r'^rotate based on position of letter ([a-z])$', line)
        if m:
            x = password.index(m.group(1)) + 1
            if x >= 5:
                x += 1
            x %= len(password)
            password = password[-x:]+password[:-x]
            continue
        m = re.search(r'^reverse positions (\d+) through (\d+)$', line)
        if m:
            x, y = map(int, m.groups())
            password[x:y+1] = reversed(password[x:y+1])
            continue
        m = re.search(r'^move position (\d+) to position (\d+)$', line)
        if m:
            x, y = map(int, m.groups())
            l = password.pop(x)
            password.insert(y, l)
            continue
        raise ValueError("Unknown operation: "+line)
    return ''.join(password)
# end scramble

def unscramble(password, ops):
    password = list(password)
    for line in reversed(ops):
        #print ''.join(password)
        m = re.search(r'^swap position (\d+) with position (\d+)$', line)
        if m:
            x, y = map(int, m.groups())
            password[x], password[y] = password[y], password[x]
            continue
        m = re.search(r'^swap letter ([a-z]) with letter ([a-z])$', line)
        if m:
            x, y = [password.index(l) for l in m.groups()]
            password[x], password[y] = password[y], password[x]
            continue
        m = re.search(r'^rotate (left|right) (\d+) steps?$', line)
        if m:
            x = -int(m.group(2))
            if m.group(1) == 'left':
                x = -x
            x %= len(password)
            password = password[-x:]+password[:-x]
            continue
        m = re.search(r'^rotate based on position of letter ([a-z])$', line)
        if m:
            y = password.index(m.group(1))
            possible = []
            for i in xrange(len(password)):
                x = i+1
                if x >= 5:
                    x += 1
                if (i + x) % len(password) == y:
                    possible.append(i)
            assert len(possible) == 1
            x = possible[0] - y
            x %= len(password)
            password = password[-x:]+password[:-x]
            continue
        m = re.search(r'^reverse positions (\d+) through (\d+)$', line)
        if m:
            x, y = map(int, m.groups())
            password[x:y+1] = reversed(password[x:y+1])
            continue
        m = re.search(r'^move position (\d+) to position (\d+)$', line)
        if m:
            x, y = map(int, m.groups())
            l = password.pop(y)
            password.insert(x, l)
            continue
        raise ValueError("Unknown operation: "+line)
    return ''.join(password)
# end unscramble

def part1(ops):
    return scramble('abcdefgh',ops)
# end part1

def part2(ops):
    return unscramble('fbgdceah',ops)
# end part2

if __name__ == '__main__':
    ops = get_input()
    print part1(ops)
    print part2(ops)

