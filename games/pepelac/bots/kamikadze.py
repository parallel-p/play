import sys


n = int(input())

area = [[0 for i in range(n + 1)] for j in range(n + 1)]


def sp(area, k):
    s = k + 0
    xb, xe, yb, ye = 1, n, 1, n
    while s < 0:
        for x in range(xb, xe + 1):
            if s < 0:
                area[yb][x] = '*'
                s += 1
        for y in range(yb + 1, ye + 1):
            if s < 0:
                area[y][xe] = '*'
                s += 1
        for x in range(xb, xe):
            if s < 0:
                area[ye][xe - x + xb - 1] = '*'
                s += 1
        for y in range(yb, ye - 1):
            if s < 0:
                area[ye - y + yb - 1][xb] = '*'
                s += 1
        xe -= 1
        xb += 1
        ye -= 1
        yb += 1

while True:
    p, b, k = tuple(map(int, input().split()))
    x, y = tuple(map(int, input().split()))[:2]

    sp(area, k)

    if p == 2:
        x2, y2 = tuple(map(int, input().split()))[:2]
    else:
        x2, y2 = -1, -1

    [input() for i in range(b)]

    if x > 1 and not (x2 == x - 1 and y2 == y) and area[y][x - 1] != '*':
        print('LEFT')
    elif y > 1 and not (y2 == y - 1 and x2 == x) and area[y - 1][x] != '*':
        print('UP')
    else:
        print('STAND')
    sys.stdout.flush()
