import re
import md5


def get_input():
    with open('day14.txt') as fp:
        input = fp.read().strip()
    
    return input
# end get_input

def gethash(salt,i,stretch=0):
    hash = md5.md5(salt+str(i)).hexdigest()
    for i in xrange(stretch):
        hash = md5.md5(hash).hexdigest()
    return hash
# end get hash

def findkeys(salt, stretch=0):
    offset = 0
    buffer = []
    for i in xrange(1001):
        buffer.append(gethash(salt,i,stretch))
    keys = []
    while len(keys) < 64:
        m = re.search(r'(.)\1\1',buffer[0])
        if m:
            digit5 = m.group(1)*5
            for hash in buffer[1:]:
                if digit5 in hash:
                    keys.append((offset,buffer[0]))
                    print len(keys), offset
                    break
        offset += 1
        buffer.pop(0)
        buffer.append(gethash(salt,offset+len(buffer),stretch))
    return keys
# end findkeys

def part1(salt):
    return findkeys(salt)[-1][0]
# end part1

def part2(salt):
    return findkeys(salt,2016)[-1][0]
# end part2

if __name__ == '__main__':
    salt = get_input()
    print part1(salt)
    print part2(salt)

