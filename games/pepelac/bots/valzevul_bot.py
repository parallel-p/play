import sys


__author__ = "Vadim D. Drobinin (vadim@drobinin.com)"


def update_info():
    '''
    Update information about state of the playing field.
    '''
    global players, bullets, armageddon
    global current_x, current_y, current_bullets
    global enemy_x, enemy_y, enemy_bullets
    global bullets_locations, current_location
    (players, bullets, armageddon) = map(int, input().split())
    (current_x, current_y, current_bullets) = map(int, input().split())
    if players > 1:
        (enemy_x, enemy_y, enemy_bullets) = map(int, input().split())
    current_location = (current_x, current_y)


def update_target():
    '''
    Update information about location of the current target.
    '''
    global bullets_locations, current_location
    global current_target, bullets
    bullets_locations = []
    for bullet in range(bullets):
        (x, y) = map(int, input().split())
        bullets_locations.append((x, y))
    target = bullets_locations[0]
    for bullet in bullets_locations:
        if shortest(bullet, current_location) < shortest(target, \
                                                current_location):
            target = bullet
    return target


def shortest(current_location, distation):
    '''
    Calculates the Hamming distance between two bullets.
    '''
    return abs(current_location[0] - distation[0]) \
            + abs(current_location[1] - distation[1])


def go(current_location, current_target):
    '''
    Return new step.
    '''
    new_x = current_target[0] - current_location[0]
    new_y = current_target[1] - current_location[1]
    if abs(new_x) > abs(new_y):
        if new_x < 0:
            return 0
        else:
            return 1
    else:
        if new_y < 0:
            return 2
        else:
            return 3


def all_is_ok():
    '''
    Check the situation in the game.
    '''
    global armageddon, bullets, players
    global current_bullets, enemy_bullets
    if (bullets == 0):
        if (current_bullets >= enemy_bullets):
            return 1
        else:
            return -1
    else:
        if (players == 1):
            return 1
        if (current_bullets >= bullets + enemy_bullets):
            return 2
        if (current_bullets + bullets < enemy_bullets):
            return -1
        else:
            return 0


STEP = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'STAND']
N = int(input())
players, bullets, armageddon = 2, 50, 10  # Default values
current_target, current_x, current_y, enemy_x, enemy_y = (0, 0), 0, 0, 0, 0
current_location, current_bullets = (current_x, current_y), 0
enemy_location, enemy_bullets = (enemy_x, enemy_y), 0
asylum = (N // 2, N // 2)
update_info()
while all_is_ok() == 0:
    current_target = update_target()
    print(STEP[go(current_location, current_target)])
    sys.stdout.flush()
    update_info()
while all_is_ok() == -1:
    if bullets > 0:
        current_target = update_target()
    asylum = (N // 2, N // 2 - 2)
    if current_location != asylum:
        print(STEP[go(current_location, asylum)])
    else:
        print(STEP[4])
    update_info()
    sys.stdout.flush()
while all_is_ok() == 2:
    if bullets > 0:
        current_target = update_target()
    target = enemy_location
    print(STEP[go(current_location, target)])
    update_info()
    sys.stdout.flush()
while True:
    if bullets > 0:
        current_target = update_target()
    if current_location != asylum:
        print(STEP[go(current_location, asylum)])
    else:
        print(STEP[4])
    update_info()
    sys.stdout.flush()
