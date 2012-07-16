import sys


n = input()

while True:
    p, b, k = tuple(map(int, input().split()))
    x, y = tuple(map(int, input().split()))[:2]

    if p == 2:
        x2, y2 = tuple(map(int, input().split()))[:2]
    else:
        x2, y2 = -1, -1

    [input() for i in range(b)]

    if x > 1 and not (x2 == x - 1 and y2 == y):
        print('LEFT')
    elif y > 1 and not (y2 == y - 1 and x2 == x):
        print('UP')
    else:
        print('STAND')
    sys.stdout.flush()
