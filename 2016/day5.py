import re
import md5


def get_input():
    with open('day5.txt') as fp:
        input = fp.read().strip()
    
    return input
# end get_input

def part1(doorid):
    i = 0
    password = ''
    while len(password) < 8:
        hash = md5.md5(doorid+str(i)).hexdigest()
        if hash[:5] == '00000':
            password += hash[5]
            print password
        i += 1
    return password
# end part1

def part2(doorid):
    i = 0
    password = [None]*8
    while None in password:
        hash = md5.md5(doorid+str(i)).hexdigest()
        if hash[:5] == '00000' and hash[5].isdigit() and int(hash[5]) < 8 and password[int(hash[5])] is None:
            password[int(hash[5])] = hash[6]
            print ''.join('_' if not c else c for c in password)
        i += 1
    return ''.join(password)
# end part2

if __name__ == '__main__':
    doorid = get_input()
    print part1(doorid)
    print part2(doorid)

