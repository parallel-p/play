import sys


input()

while True:
    input()
    x, y = tuple(map(int, input().split()))[:2]

    while not x == y == 1:
        if x > 1:
            x -= 1
            print('LEFT')
            sys.stdout.flush()
        elif y > 1:
            y -= 1
            print('UP')
            sys.stdout.flush()
    print('STAY')
    sys.stdout.flush()
