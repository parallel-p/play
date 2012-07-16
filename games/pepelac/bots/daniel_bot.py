import sys
from random import randint
import datetime

global_log_file = open('/home/daniel/play/play/qogdaniel.log', 'w')

FIELD_SIZE = int(input())

PLAYERS_COUNT = 2
LUZ_COUNT = None
TIME_LEFT = None
mX, mY, mLUZ = None, None, None
oX, oY, oLUZ = None, None, None
LUZ_LIST = []


def flush(dir):
    if dir[0] > 0:
        dir = 4
    elif dir[0] < 0:
        dir = 2
    elif dir[1] < 0:
        dir = 3
    elif dir[1] > 0:
        dir = 1
    else:
        dir = 0
    print(['STAND', 'RIGHT', 'UP', 'LEFT', 'DOWN'][dir])
    sys.stdout.flush()


def log(s):
    global global_log_file
    print(s, file=global_log_file)
    global_log_file.flush()


def logAll():
    log("Field size " + str(FIELD_SIZE) + " luz count " + str(LUZ_COUNT) + ", time left " + str(TIME_LEFT))
    log("My x " + str(mX) + ", my y " + str(mY) + ", my luz " + str(mLUZ))
    log("Other x " + str(mX) + ", other y " + str(mY) + ", other luz " + str(mLUZ))
    log(LUZ_LIST)


def update():
    global PLAYERS_COUNT, LUZ_COUNT, TIME_LEFT, mX, mY, mLUZ, oX, oY, oLUZ
    global LUZ_LIST

    PLAYERS_COUNT, LUZ_COUNT, TIME_LEFT = [int(x) for x in input().split()]
    mX, mY, mLUZ = [int(x) for x in input().split()]
    oX, oY, oLUZ = [int(x) for x in input().split()]
    LUZ_LIST = []
    for i in range(LUZ_COUNT):
        x, y = input().split()
        LUZ_LIST.append((int(x), int(y)))


def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0


def sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def randfix(x):
    a, b = x[0], x[1]
    if a and b:
        if randint(0, 1):
            a = 0
        else:
            b = 0
    return (a, b)


def towards(to):
    danger = mLUZ <= oLUZ
    nX, nY = sign(to[0] - mX), sign(to[1] - mY)
    return randfix((nX, nY))
    if not danger:
        if (abs(mX - oX) == 1) and (abs(mY - oY) == 1):
            return randfix(sub((oX, oY), (mX, mY)))
        if nX and nY:
            if mX == oX:
                return (0, nY)
            elif mY == oY:
                return (nX, 0)
            else:
                return randfix((nX, nY))
        elif nX:
            if mX == oX:
                return (0, [-1, 1][randint(0, 1)])
            else:
                return (nX, 0)
        elif nY:
            if mY == oY:
                return ([-1, 1][randint(0, 1)], 0)
            else:
                return (0, nY)

gX, gY = int(FIELD_SIZE / 2) + 1, int(FIELD_SIZE / 2) + [1, 0][FIELD_SIZE % 2]
finish = (gX, gY)

SLOWPOKE = 0

while True:
    # logAll()
    update()
    if LUZ_COUNT:
        me = (mX, mY)
        life_dist = dist(finish, me)
        luz_dist = 100000000000000000
        gut_luz = None
        for luz in LUZ_LIST:
            d = dist((mX, mY), luz)
            if d < luz_dist:
                luz_dist = d
                gut_luz = luz
        log("luz_dist " + str(luz_dist + dist(gut_luz, finish)))
        log("life_dist " + str(life_dist))

        if luz_dist + dist(gut_luz, finish) + SLOWPOKE < TIME_LEFT:
            flush(towards(gut_luz))
        else:
            flush(towards(finish))
    else:
        flush(towards(finish))



# def bfs(pos):
#     queue = deque()
#     queue.append(pos)
#     visited = {pos: 0}
#     while queue:
#         curr = queue.popleft()
#         if not curr in visited:
#             visited[pos] = 0
#             if curr[0] > 1:
#                 if curr[1] > 1:
#                     queue.append((curr[0] - 1, curr[1] - 1))
#                 if curr[1] < FIELD_SIZE:
#                     queue.append((curr[0] - 1, curr[1] + 1))
#             if curr[0] < FIELD_SIZE:
#                 if curr[1] > 1:
#                     queue.append((curr[0] + 1, curr[1] - 1))
#                 if curr[1] < FIELD_SIZE:
#                     queue.append((curr[0] + 1, curr[1] + 1))
