import re


def get_input():
    with open('day10.txt') as fp:
        input = fp.read().strip()
    
    return input.split('\n')
# end get_input

def setup(lines):
    bots = {}
    rules = {}
    ready = []
    for line in lines:
        m = re.search(r'^value (\d+) goes to bot (\d+)$', line)
        if m:
            bot = int(m.group(2))
            bots.setdefault(bot,[]).append(int(m.group(1)))
            if len(bots[bot]) == 2:
                ready.append(bot)
        else:
            m = re.search(r'^bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)$', line)
            bot = int(m.group(1))
            assert bot not in rules
            rules[bot] = ((m.group(2), int(m.group(3))), (m.group(4), int(m.group(5))))
    return bots, rules, ready
# end setup

def process(bots, rules, ready):
    outputs = {}
    while ready:
        bot = ready.pop(0)
        assert len(bots[bot]) == 2
        bots[bot].sort()
        for i, (type, num) in enumerate(rules[bot]):
            if type == 'bot':
                bots.setdefault(num,[]).append(bots[bot][i])
                if len(bots[num]) == 2:
                    ready.append(num)
            else:
                assert num not in outputs
                outputs[num] = bots[bot][i]
    return bots, outputs
# end process

def part1(bots):
    for bot in bots:
        if bots[bot] == [17,61]:
            return bot
# end part1

def part2(outputs):
    return outputs[0]*outputs[1]*outputs[2]
# end part2

if __name__ == '__main__':
    lines = get_input()
    bots, rules, ready = setup(lines)
    bots, outputs = process(bots, rules, ready)
    print part1(bots)
    print part2(outputs)

