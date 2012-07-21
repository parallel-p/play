import sys


def get_distance(my_x, my_y, dest_x, dest_y):
    return abs(my_x - dest_x) + abs(my_y - dest_y)


def make_move(my_x, my_y, dest_x, dest_y):
    if abs(dest_x - my_x) < abs(dest_y - my_y):
        if my_y > dest_y:
            print('LEFT')
        elif dest_y > my_y:
            print('RIGHT')
    else:
        if my_x > dest_x:
            print('UP')
        elif dest_x > my_x:
            print('DOWN')
        else:
            print('STAND')
    sys.stdout.flush()


def determine_target(my_x, my_y, targets):
    result = targets[0]
    for target in targets:
        if len(targets[0]) == 3 and (targets[0][2] > target[2] or (
                targets[0][2] == target[2] and get_distance(
                    my_x, my_y, target[0], target[1]) < get_distance(
                        my_x, my_y, result[0], result[1]))):
            result = target
        elif len(targets[0]) == 2 and get_distance(
                my_x, my_y, target[0], target[1]) < get_distance(
                    my_x, my_y, result[0], result[1]):
            result = target
    return result


def main():
    ''' Strategy:
        if there are some bullets, gather them;
            but if we have more bullets, than the enemy does and
            we can reach him before he finds one, go and kill him.
        if there are no bullets, go and attack the enemy. '''
    n = int(input())
    while True:
        input1 = input()
        input2 = input()
        (players, bullet_num, k) = map(int, input1.split())
        (my_x, my_y, my_bullets) = map(int, input2.split())
        enemies = []
        for i in range(players - 1):
            inputt = input()
            enemy = tuple(map(int, inputt.split()))
            enemies.append(enemy)
        bullets = []
        for i in range(bullet_num):
            inputt = input()
            bullet = tuple(map(int, inputt.split()))
            bullets.append(bullet)
        if bullet_num > 0:
            for enemy in enemies:
                enemy_bullet = determine_target(
                    enemy[0], enemy[1], bullets)
                if enemy[2] < my_bullets and get_distance(
                        enemy[0], enemy[1],
                        enemy_bullet[0],
                        enemy_bullet[1]) > get_distance(
                            my_x, my_y, enemy[0], enemy[1]):
                                # If I find an enemy, whose ammo is lower,
                                # than mine and I would reach him before he
                                # gets a bullet, I'll go and kill him.
                                make_move(my_x, my_y, enemy[0], enemy[1])
                                continue
            # And if there isn't such one, I'll just collect bullets.
            bullet = determine_target(my_x, my_y, bullets)
            make_move(my_x, my_y, bullet[0], bullet[1])
        else:
            if len(enemies) == 0:
                make_move(my_x, my_y, n // 2, n // 2)
                # If I'm alone, I'll go to the center.
            else:
                # When there are no bullets left, if I have less ammo, than
                # enemies do, I will lose no matter what I do. So, a suicide
                # attack is better here.
                target = determine_target(my_x, my_y, enemies)
                make_move(my_x, my_y, target[0], target[1])


if __name__ == '__main__':
    main()

