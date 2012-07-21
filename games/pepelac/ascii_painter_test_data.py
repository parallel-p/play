# -*- coding: utf-8 -*-
from unittest.mock import Mock

good = Mock(bot_name='GoodBot', author_name='Longcat')
bad  = Mock(bot_name='BadBot', author_name='Tacgnol')
dead = Mock(bot_name='DeadBot', author_name='Tima')

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
        'players': [good, bad, dead],
        'bullets': [6, 3, 0],
        'dead': [dead],
        'why_dead': {dead:0},
        'scores': {good: 42, bad: 42, dead: 3},
        'collisions': None,

        'result': '\x1b[41m\x1b[33m\x1b[1m@@@@@@@@@@@@\x1b[0m\n\x1b[42m\x1b[36m\x1b[22m[][]\x1b[45m\x1b[37m\x1b[1mP0\x1b[42m\x1b[36m\x1b[22m[]\x1b[43m\x1b[30m\x1b[22m**\x1b[41m\x1b[33m\x1b[1m@@\x1b[0m\n\x1b[42m\x1b[36m\x1b[22m[]\x1b[43m\x1b[30m\x1b[22m**\x1b[42m\x1b[36m\x1b[22m[][][]\x1b[41m\x1b[33m\x1b[1m@@\x1b[0m\n\x1b[42m\x1b[36m\x1b[22m[][][][][]\x1b[45m\x1b[37m\x1b[1mP1\x1b[0m\n\x1b[43m\x1b[30m\x1b[22m**\x1b[42m\x1b[36m\x1b[22m[][]\x1b[43m\x1b[30m\x1b[22m**\x1b[42m\x1b[36m\x1b[22m[][]\x1b[0m\n\x1b[42m\x1b[36m\x1b[22m[][]\x1b[43m\x1b[30m\x1b[22m**\x1b[42m\x1b[36m\x1b[22m[][]\x1b[43m\x1b[30m\x1b[22m**\x1b[0m\n\n\x1b[44m\x1b[33m\x1b[1mPlayers in game:\x1b[0m\n\x1b[40m\x1b[37m\x1b[1m[P0]\x1b[32m\x1b[22mGoodBot        \x1b[33m\x1b[22m by \x1b[36mLongcat             \x1b[33m\x1b[22m has \x1b[35m   6\x1b[33m\x1b[22m bullets                                 \x1b[0m\n\x1b[40m\x1b[37m\x1b[1m[P1]\x1b[32m\x1b[22mBadBot         \x1b[33m\x1b[22m by \x1b[36mTacgnol             \x1b[33m\x1b[22m has \x1b[35m   3\x1b[33m\x1b[22m bullets                                 \x1b[0m\n\x1b[41m\x1b[37m\x1b[1m[P2]\x1b[32m\x1b[22mDeadBot        \x1b[33m\x1b[22m by \x1b[36mTima                \x1b[33m\x1b[22m is dead (\x1b[35m burnt in Armageddon \x1b[33m\x1b[22m), with score \x1b[35m   3\x1b[33m\x1b[22m \x1b[0m\n'
    }

]
