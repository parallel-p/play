# -*- coding: utf-8 -*-
from unittest.mock import Mock


good = Mock(bot_name='GoodBot',author_name='Serious Cat')
bad =  Mock(bot_name='BadBot',author_name='Nyan Cat')
dead = Mock(bot_name='DeadBot',author_name='Tima')
zerg = [ Mock(bot_name='ZergBot{:02d}'.format(n), author_name='LongCat') for n in range(100)]

tests = [

    {
        'field': [
            [-2, -2, -2, -2, -2, -2],
            [0,  0,  1,  0, -1, -2],
            [0, -1,  0,  0,  0, -2],
            [0,  0,  0,  0,  0,  2],
            [-1,  0,  0, -1,  0,  0],
            [0,  0, -1,  0,  0, -1]
        ],
        'players' : [good, bad, dead],
        'bullets' : [6, 3, 0],
        'dead' : [dead],
        'why_dead' : {dead:0},
        'scores' : {good: 42, bad: 42, dead: 3},
        'collisions' : None,
        
        'result' : '\x1b[41m\x1b[33m\x1b[1m@@@@@@@@@@@@\x1b[0m\n\x1b[42m\x1b[36m\x1b[22m[][]\x1b[45m\x1b[37m\x1b[1mP0\x1b[42m\x1b[36m\x1b[22m[]\x1b[43m\x1b[30m\x1b[22m**\x1b[41m\x1b[33m\x1b[1m@@\x1b[0m\n\x1b[42m\x1b[36m\x1b[22m[]\x1b[43m\x1b[30m\x1b[22m**\x1b[42m\x1b[36m\x1b[22m[][][]\x1b[41m\x1b[33m\x1b[1m@@\x1b[0m\n\x1b[42m\x1b[36m\x1b[22m[][][][][]\x1b[45m\x1b[37m\x1b[1mP1\x1b[0m\n\x1b[43m\x1b[30m\x1b[22m**\x1b[42m\x1b[36m\x1b[22m[][]\x1b[43m\x1b[30m\x1b[22m**\x1b[42m\x1b[36m\x1b[22m[][]\x1b[0m\n\x1b[42m\x1b[36m\x1b[22m[][]\x1b[43m\x1b[30m\x1b[22m**\x1b[42m\x1b[36m\x1b[22m[][]\x1b[43m\x1b[30m\x1b[22m**\x1b[0m\n\n\x1b[44m\x1b[33m\x1b[1mPlayers in game:\x1b[0m\n\x1b[40m\x1b[37m\x1b[1m[P0]\x1b[32m\x1b[22mGoodBot        \x1b[33m\x1b[22m by \x1b[36mSerious Cat         \x1b[33m\x1b[22m has \x1b[35m   6\x1b[33m\x1b[22m bullets                                      \x1b[0m\n\x1b[40m\x1b[37m\x1b[1m[P1]\x1b[32m\x1b[22mBadBot         \x1b[33m\x1b[22m by \x1b[36mNyan Cat            \x1b[33m\x1b[22m has \x1b[35m   3\x1b[33m\x1b[22m bullets                                      \x1b[0m\n\x1b[41m\x1b[37m\x1b[1m[P2]\x1b[32m\x1b[22mDeadBot        \x1b[33m\x1b[22m by \x1b[36mTima                \x1b[33m\x1b[22m is dead (\x1b[35m burnt in Armageddon      \x1b[33m\x1b[22m), with score \x1b[35m   3\x1b[33m\x1b[22m \x1b[0m\n'

    },

    {
        'field' : [
        [-2, -2, -2, -2, -2, -2],
        [ 0,  0,  0,  0, -1, -2],
        [ 0, -1,  0,  0,  0, -2],
        [ 0,  0,  1,  2,  0, -2],
        [-1,  0,  0, -1,  0, -2],
        [ 0,  0, -1,  0,  0, -1]
        ],

        'players' : [good, bad, dead],
        'bullets' : [6, 3, 0],
        'dead' : [dead],
        'why_dead' : {dead:0},
        'scores' : {good: 44, bad: 44, dead: 3},
        'collisions' : [good,bad],

        'result' : '\x1b[41m\x1b[33m\x1b[1m@@@@@@@@@@@@\x1b[0m\n\x1b[42m\x1b[36m\x1b[22m[][][][]\x1b[43m\x1b[30m\x1b[22m**\x1b[41m\x1b[33m\x1b[1m@@\x1b[0m\n\x1b[42m\x1b[36m\x1b[22m[]\x1b[43m\x1b[30m\x1b[22m**\x1b[42m\x1b[36m\x1b[22m[][][]\x1b[41m\x1b[33m\x1b[1m@@\x1b[0m\n\x1b[42m\x1b[36m\x1b[22m[][]\x1b[41m\x1b[33m\x1b[1mP0P1\x1b[42m\x1b[36m\x1b[22m[]\x1b[41m\x1b[33m\x1b[1m@@\x1b[0m\n\x1b[43m\x1b[30m\x1b[22m**\x1b[42m\x1b[36m\x1b[22m[][]\x1b[43m\x1b[30m\x1b[22m**\x1b[42m\x1b[36m\x1b[22m[]\x1b[41m\x1b[33m\x1b[1m@@\x1b[0m\n\x1b[42m\x1b[36m\x1b[22m[][]\x1b[43m\x1b[30m\x1b[22m**\x1b[42m\x1b[36m\x1b[22m[][]\x1b[43m\x1b[30m\x1b[22m**\x1b[0m\n\n\x1b[44m\x1b[33m\x1b[1mPlayers in game:\x1b[0m\n\x1b[40m\x1b[37m\x1b[1m[P0]\x1b[32m\x1b[22mGoodBot        \x1b[33m\x1b[22m by \x1b[36mSerious Cat         \x1b[33m\x1b[22m has \x1b[35m   6\x1b[33m\x1b[22m bullets                                      \x1b[0m\n\x1b[40m\x1b[37m\x1b[1m[P1]\x1b[32m\x1b[22mBadBot         \x1b[33m\x1b[22m by \x1b[36mNyan Cat            \x1b[33m\x1b[22m has \x1b[35m   3\x1b[33m\x1b[22m bullets                                      \x1b[0m\n\x1b[41m\x1b[37m\x1b[1m[P2]\x1b[32m\x1b[22mDeadBot        \x1b[33m\x1b[22m by \x1b[36mTima                \x1b[33m\x1b[22m is dead (\x1b[35m burnt in Armageddon      \x1b[33m\x1b[22m), with score \x1b[35m   3\x1b[33m\x1b[22m \x1b[0m\n'

    },

    {
        'field' : [
        [-2, -2, -2, -2, 24,  9],
        [ 1,  0,  0,  7,  0,  0],
        [ 0, -1, 14,  8,  0, 10],
        [12,  0,  2,  0,  6,  0],
        [ 0, 11,  0, 23,  0,  0],
        [17,  0,  0,  4,  0, 20]
        ],

        'players' : zerg[:25],
        'bullets' : [0,0,0,2,0,0,3,0,3,2,2,1,0,1,0,0,0,0,0,3,0,0,0,2,0],
        'dead' : [zerg[2],zerg[4],zerg[12],zerg[14],zerg[15],zerg[17],zerg[18],zerg[20],zerg[21],zerg[24]],
        'why_dead' : {zerg[2]:1, zerg[4]:0, zerg[12]:1, zerg[14]:1, zerg[15]:-1, zerg[17]:1, zerg[18]:-1, zerg[20]:0, zerg[21]:1, zerg[24]:1},
        'scores' : {zerg[0]:14, zerg[1]:14, zerg[2]:3, zerg[3]:14, zerg[4]:11,
                    zerg[5]:14, zerg[6]:14, zerg[7]:14, zerg[8]:14, zerg[9]:14,
                    zerg[10]:14, zerg[11]:14, zerg[12]:9, zerg[13]:14, zerg[14]:10,
                    zerg[15]:0, zerg[16]:14, zerg[17]:9, zerg[18]:1, zerg[19]:14,
                    zerg[20]:12, zerg[21]:9, zerg[22]:14, zerg[23]:14, zerg[24]:11},
        'collisions' : [zerg[1], zerg[3], zerg[7], zerg[8], zerg[6], zerg[13], zerg[22], zerg[23]],

        'result' : '\x1b[41m\x1b[33m\x1b[1m@@@@@@@@PnP8\x1b[0m\n\x1b[45m\x1b[37m\x1b[1mP0\x1b[42m\x1b[36m\x1b[22m[][]\x1b[41m\x1b[33m\x1b[1mP6\x1b[42m\x1b[36m\x1b[22m[][]\x1b[0m\n\x1b[42m\x1b[36m\x1b[22m[]\x1b[43m\x1b[30m\x1b[22m**\x1b[41m\x1b[33m\x1b[1mPdP7\x1b[42m\x1b[36m\x1b[22m[]\x1b[45m\x1b[37m\x1b[1mP9\x1b[0m\n\x1b[45m\x1b[37m\x1b[1mPb\x1b[42m\x1b[36m\x1b[22m[]\x1b[41m\x1b[33m\x1b[1mP1\x1b[42m\x1b[36m\x1b[22m[]\x1b[45m\x1b[37m\x1b[1mP5\x1b[42m\x1b[36m\x1b[22m[]\x1b[0m\n\x1b[42m\x1b[36m\x1b[22m[]\x1b[45m\x1b[37m\x1b[1mPa\x1b[42m\x1b[36m\x1b[22m[]\x1b[41m\x1b[33m\x1b[1mPm\x1b[42m\x1b[36m\x1b[22m[][]\x1b[0m\n\x1b[45m\x1b[37m\x1b[1mPg\x1b[42m\x1b[36m\x1b[22m[][]\x1b[41m\x1b[33m\x1b[1mP3\x1b[42m\x1b[36m\x1b[22m[]\x1b[45m\x1b[37m\x1b[1mPj\x1b[0m\n\n\x1b[44m\x1b[33m\x1b[1mPlayers in game:\x1b[0m\n\x1b[40m\x1b[37m\x1b[1m[P0]\x1b[32m\x1b[22mZergBot00      \x1b[33m\x1b[22m by \x1b[36mLongCat             \x1b[33m\x1b[22m has \x1b[35m   0\x1b[33m\x1b[22m bullets                                      \x1b[0m\n\x1b[40m\x1b[37m\x1b[1m[P1]\x1b[32m\x1b[22mZergBot01      \x1b[33m\x1b[22m by \x1b[36mLongCat             \x1b[33m\x1b[22m has \x1b[35m   0\x1b[33m\x1b[22m bullets                                      \x1b[0m\n\x1b[41m\x1b[37m\x1b[1m[P2]\x1b[32m\x1b[22mZergBot02      \x1b[33m\x1b[22m by \x1b[36mLongCat             \x1b[33m\x1b[22m is dead (\x1b[35m killed in fight          \x1b[33m\x1b[22m), with score \x1b[35m   3\x1b[33m\x1b[22m \x1b[0m\n\x1b[40m\x1b[37m\x1b[1m[P3]\x1b[32m\x1b[22mZergBot03      \x1b[33m\x1b[22m by \x1b[36mLongCat             \x1b[33m\x1b[22m has \x1b[35m   2\x1b[33m\x1b[22m bullets                                      \x1b[0m\n\x1b[41m\x1b[37m\x1b[1m[P4]\x1b[32m\x1b[22mZergBot04      \x1b[33m\x1b[22m by \x1b[36mLongCat             \x1b[33m\x1b[22m is dead (\x1b[35m burnt in Armageddon      \x1b[33m\x1b[22m), with score \x1b[35m  11\x1b[33m\x1b[22m \x1b[0m\n\x1b[40m\x1b[37m\x1b[1m[P5]\x1b[32m\x1b[22mZergBot05      \x1b[33m\x1b[22m by \x1b[36mLongCat             \x1b[33m\x1b[22m has \x1b[35m   0\x1b[33m\x1b[22m bullets                                      \x1b[0m\n\x1b[40m\x1b[37m\x1b[1m[P6]\x1b[32m\x1b[22mZergBot06      \x1b[33m\x1b[22m by \x1b[36mLongCat             \x1b[33m\x1b[22m has \x1b[35m   3\x1b[33m\x1b[22m bullets                                      \x1b[0m\n\x1b[40m\x1b[37m\x1b[1m[P7]\x1b[32m\x1b[22mZergBot07      \x1b[33m\x1b[22m by \x1b[36mLongCat             \x1b[33m\x1b[22m has \x1b[35m   0\x1b[33m\x1b[22m bullets                                      \x1b[0m\n\x1b[40m\x1b[37m\x1b[1m[P8]\x1b[32m\x1b[22mZergBot08      \x1b[33m\x1b[22m by \x1b[36mLongCat             \x1b[33m\x1b[22m has \x1b[35m   3\x1b[33m\x1b[22m bullets                                      \x1b[0m\n\x1b[40m\x1b[37m\x1b[1m[P9]\x1b[32m\x1b[22mZergBot09      \x1b[33m\x1b[22m by \x1b[36mLongCat             \x1b[33m\x1b[22m has \x1b[35m   2\x1b[33m\x1b[22m bullets                                      \x1b[0m\n\x1b[40m\x1b[37m\x1b[1m[Pa]\x1b[32m\x1b[22mZergBot10      \x1b[33m\x1b[22m by \x1b[36mLongCat             \x1b[33m\x1b[22m has \x1b[35m   2\x1b[33m\x1b[22m bullets                                      \x1b[0m\n\x1b[40m\x1b[37m\x1b[1m[Pb]\x1b[32m\x1b[22mZergBot11      \x1b[33m\x1b[22m by \x1b[36mLongCat             \x1b[33m\x1b[22m has \x1b[35m   1\x1b[33m\x1b[22m bullets                                      \x1b[0m\n\x1b[41m\x1b[37m\x1b[1m[Pc]\x1b[32m\x1b[22mZergBot12      \x1b[33m\x1b[22m by \x1b[36mLongCat             \x1b[33m\x1b[22m is dead (\x1b[35m killed in fight          \x1b[33m\x1b[22m), with score \x1b[35m   9\x1b[33m\x1b[22m \x1b[0m\n\x1b[40m\x1b[37m\x1b[1m[Pd]\x1b[32m\x1b[22mZergBot13      \x1b[33m\x1b[22m by \x1b[36mLongCat             \x1b[33m\x1b[22m has \x1b[35m   1\x1b[33m\x1b[22m bullets                                      \x1b[0m\n\x1b[41m\x1b[37m\x1b[1m[Pe]\x1b[32m\x1b[22mZergBot14      \x1b[33m\x1b[22m by \x1b[36mLongCat             \x1b[33m\x1b[22m is dead (\x1b[35m killed in fight          \x1b[33m\x1b[22m), with score \x1b[35m  10\x1b[33m\x1b[22m \x1b[0m\n\x1b[41m\x1b[37m\x1b[1m[Pf]\x1b[32m\x1b[22mZergBot15      \x1b[33m\x1b[22m by \x1b[36mLongCat             \x1b[33m\x1b[22m is dead (\x1b[35m stepped somewhere wrong  \x1b[33m\x1b[22m), with score \x1b[35m   0\x1b[33m\x1b[22m \x1b[0m\n\x1b[40m\x1b[37m\x1b[1m[Pg]\x1b[32m\x1b[22mZergBot16      \x1b[33m\x1b[22m by \x1b[36mLongCat             \x1b[33m\x1b[22m has \x1b[35m   0\x1b[33m\x1b[22m bullets                                      \x1b[0m\n\x1b[41m\x1b[37m\x1b[1m[Ph]\x1b[32m\x1b[22mZergBot17      \x1b[33m\x1b[22m by \x1b[36mLongCat             \x1b[33m\x1b[22m is dead (\x1b[35m killed in fight          \x1b[33m\x1b[22m), with score \x1b[35m   9\x1b[33m\x1b[22m \x1b[0m\n\x1b[41m\x1b[37m\x1b[1m[Pi]\x1b[32m\x1b[22mZergBot18      \x1b[33m\x1b[22m by \x1b[36mLongCat             \x1b[33m\x1b[22m is dead (\x1b[35m stepped somewhere wrong  \x1b[33m\x1b[22m), with score \x1b[35m   1\x1b[33m\x1b[22m \x1b[0m\n\x1b[40m\x1b[37m\x1b[1m[Pj]\x1b[32m\x1b[22mZergBot19      \x1b[33m\x1b[22m by \x1b[36mLongCat             \x1b[33m\x1b[22m has \x1b[35m   3\x1b[33m\x1b[22m bullets                                      \x1b[0m\n\x1b[41m\x1b[37m\x1b[1m[Pk]\x1b[32m\x1b[22mZergBot20      \x1b[33m\x1b[22m by \x1b[36mLongCat             \x1b[33m\x1b[22m is dead (\x1b[35m burnt in Armageddon      \x1b[33m\x1b[22m), with score \x1b[35m  12\x1b[33m\x1b[22m \x1b[0m\n\x1b[41m\x1b[37m\x1b[1m[Pl]\x1b[32m\x1b[22mZergBot21      \x1b[33m\x1b[22m by \x1b[36mLongCat             \x1b[33m\x1b[22m is dead (\x1b[35m killed in fight          \x1b[33m\x1b[22m), with score \x1b[35m   9\x1b[33m\x1b[22m \x1b[0m\n\x1b[40m\x1b[37m\x1b[1m[Pm]\x1b[32m\x1b[22mZergBot22      \x1b[33m\x1b[22m by \x1b[36mLongCat             \x1b[33m\x1b[22m has \x1b[35m   0\x1b[33m\x1b[22m bullets                                      \x1b[0m\n\x1b[40m\x1b[37m\x1b[1m[Pn]\x1b[32m\x1b[22mZergBot23      \x1b[33m\x1b[22m by \x1b[36mLongCat             \x1b[33m\x1b[22m has \x1b[35m   2\x1b[33m\x1b[22m bullets                                      \x1b[0m\n\x1b[41m\x1b[37m\x1b[1m[Po]\x1b[32m\x1b[22mZergBot24      \x1b[33m\x1b[22m by \x1b[36mLongCat             \x1b[33m\x1b[22m is dead (\x1b[35m killed in fight          \x1b[33m\x1b[22m), with score \x1b[35m  11\x1b[33m\x1b[22m \x1b[0m\n'

   }
]
