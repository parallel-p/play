import sys
n, p, s, k = tuple(map(int, input().split()))
player = list(map(int, input().split()))
players = [list(map(int, input().split())) for i in range(s - 1)]
patrons = [list(map(int, input().split())) for i in range(p)]
area = [[0 for j in range(n + 1)] for i in range(n + 1)]
area[player[1]][player[1]] = player
for player in players:
    area[player[1]][player[0]] = player
for patron in patrons:
    area[patron[1]][patron[0]] = 1

x, y, p = player


def check(x, y):
    if area[y][x] == 1:
        return True
    elif type(area[y][x]) == list:
        return False
    elif area[y][x] == 0:
        return 2

a, b, c, d = 0, 0, 0, 0
ok = False

if x + 1 <= n:
    e = check(x + 1, y)
    if e is True:
        print('Right')
        ok = True
    elif e == 2:
        a = 1
if y + 1 <= n:
    e = check(x, y + 1)
    if not ok and e is True:
        print('Down')
    if e == 2:
        b = 1
if x - 1 <= n:
    e = check(x - 1, y)
    if not ok and e is True:
        print('Left')
    if e == 2:
        c = 1
if y - 1 <= n:
    e = check(x, y - 1)
    if not ok and e is True:
        print('Up')
    if e == 2:
        d = 1

if not ok:
    if a:
        print('Right')
    elif b:
        print('Down')
    elif b:
        print('Left')
    elif d:
        print('Up')
    else:
        print('Stay')
sys.stdout.flush()
