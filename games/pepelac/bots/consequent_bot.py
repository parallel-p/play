import sys

NONE = (-1, -1)


def make_move(current_position, current_target):
    '''
    Makes one move towards the target
    '''
    dx = current_target[0] - current_position[0]
    dy = current_target[1] - current_position[1]
    if abs(dx) > abs(dy):
        if dx < 0:
            print('UP')
        else:
            print('DOWN')
    else:
        if dy < 0:
            print('LEFT')
        else:
            print('RIGHT')
    sys.stdout.flush()



def main():
    '''
    This bot just tries to take all the bullets without thinking about
    anything else.
    '''
    n = int(input())
    current_target = NONE
    (players, bullets, k) = map(int, input().split())
    while bullets > 0:
        (curx, cury, curb) = map(int, input().split())
        #Here we just forget about others
        for player in range(players - 1):
            (tmpx, tmpy) = map(int, input().split())
        for bullet in range(bullets):
            (bx, by) = map(int, input().split())
        if current_target == (curx, cury):
            current_target = NONE
        if current_target == NONE:
            current_target = (bx, by)
        make_move((curx, cury), current_target)
        (players, bullets, k) = map(int, input().split())
    current_target = (n // 2, n // 2)
    (curx, cury, curb) = map(int, input().split())
    for player in range(players - 1):
            (tmpx, tmpy) = map(int, input().split())
    while (curx, cury) != current_target:
        make_move((curx, cury), current_target)
        (players, bullets, k) = map(int, input().split())
        (curx, cury, curb) = map(int, input().split())
        for player in range(players - 1):
            (tmpx, tmpy) = map(int, input().split())
    while True:
        print('STAND')
        sys.stdout.flush()


if __name__ == '__main__':
    main()