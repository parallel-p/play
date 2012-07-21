from math import atan2, pi
import sys
import traceback

n = int(input())

def make_move(my_pos, his_pos, rev=False):
    if my_pos[:2] == his_pos[:2]:
        return "STAND"
    angle = atan2(his_pos[0] - my_pos[0], his_pos[1] - my_pos[1]) + pi * rev
    while angle > pi:
        angle -= 2*pi
    while angle < -pi:
        angle += 2*pi
    if -pi/4 < angle <= pi/4:
        #with open('error.log', 'a') as f:
        #    print('my_pos = ', my_pos, ', target = ', his_pos, ', angle = ', angle, ', going right', file=f, sep='')
        return "RIGHT"
    elif pi/4 < angle <= 3*pi/4:
        #with open('error.log', 'a') as f:
        #    print('my_pos = ', my_pos, ', target = ', his_pos, ', angle = ', angle, ', going up', file=f, sep='')
        return "DOWN"
    elif -3*pi/4 < angle <= -pi/4:
        #with open('error.log', 'a') as f:
        #    print('my_pos = ', my_pos, ', target = ', his_pos, ', angle = ', angle, ', going down', file=f, sep='')
        return "UP"
    else:
        #with open('error.log', 'a') as f:
        #    print('my_pos = ', my_pos, ', target = ', his_pos, ', angle = ', angle, ', going left', file=f, sep='')
        return "LEFT"

def distance(me, him):
    if him is None:
        return float('inf')
    return ((me[0]-him[0])**2 + (me[1]-him[1])**2)**0.5

try:
    while True:
        p,b,k = map(int,input().split())
        my = tuple(map(int,input().split()))
        other = [None] * (p - 1)
        for i in range(p - 1):
            other[i] = tuple(map(int,input().split()))
        patron = [None] * b
        for i in range(b):
            patron[i] = tuple(map(int,input().split()))
        opp = None
        for player in other:
            if player[2] > my[2] and distance(my,player) < distance(my, opp):
                opp = player
        if distance(my, opp) <= 3:
            print(make_move(my, opp, True))
        else:
            if k <= 0:
                print(make_move(my, ((n + 1)//2, (n + 1)//2)))
            else:
                bullet = None
                for cbull in patron:
                    if distance(my, bullet) > distance(my, cbull):
                        bullet = cbull
                if bullet is not None:
                    print(make_move(my, bullet))
                else:
                    print('STAND')
        sys.stdout.flush()
except Exception:
    with open('error.log', 'a') as f:
        traceback.print_exc(file=f)