from math import atan2, pi
import sys
import traceback

n = int(input())


def make_move(my_pos, his_pos, rev=False):
    if my_pos[:2] == his_pos[:2]:
        return "STAND"
    angle = atan2(his_pos[0] - my_pos[0], his_pos[1] - my_pos[1]) + pi * rev
    while angle > pi:
        angle -= 2 * pi
    while angle < -pi:
        angle += 2 * pi
    if -pi / 4 < angle <= pi / 4:
        return "RIGHT" if my_pos[1] < n else "STAND"
    elif pi / 4 < angle <= 3 * pi / 4:
        return "DOWN" if my_pos[0] < n else "STAND"
    elif -3 * pi / 4 < angle <= -pi / 4:
        return "UP" if my_pos[0] > 1 else "STAND"
    else:
        return "LEFT" if my_pos[1] > 1 else "STAND"


def distance(me, him):
    if him is None:
        return float('inf')
    return ((me[0] - him[0]) ** 2 + (me[1] - him[1]) ** 2) ** 0.5


while True:
    p, b, k = map(int, input().split())
    my = tuple(map(int, input().split()))
    other = [None] * (p - 1)
    for i in range(p - 1):
        other[i] = tuple(map(int, input().split()))
    patron = [None] * b
    for i in range(b):
        patron[i] = tuple(map(int, input().split()))
    opp = None
    for player in other:
        if player[2] > my[2] and distance(my, player) < distance(my, opp):
            opp = player
    if distance(my, opp) <= 3:
        print(make_move(my, opp, True))
    else:
        if k <= 0 or b == 0:
            print(make_move(my, ((n + 1) // 2, (n + 1) // 2)))
        else:
            bullet = None
            for cbull in patron:
                if distance(my, bullet) > distance(my, cbull):
                    bullet = cbull
            print(make_move(my, bullet))
    sys.stdout.flush()
