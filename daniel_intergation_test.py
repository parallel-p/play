import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

GAME_PATH = 'games/nim'

import config_helpers
config_helpers.initialize_game_environment(GAME_PATH)
import config

MAIN_MOCK = MagicMock()

with patch.dict('sys.modules', {'tournament_stages.game': MAIN_MOCK}):
    import tournament_stages.game
    from tournament_stages.tournament import Tournament

import os
from inspect import getframeinfo, currentframe
# import sys


class TournamentIntegrationTest(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(GAME_PATH, 'players_config'), 'w') as file:
            file.write('''"Author Authorovich" "MegaBot" "/home/artur/bot_path"'''
                       '''Author Bot "/usr/lol"'''
                       '''Author "Bot and bot" /usr/lol'''
                       '''Author "Bot and bot'   '/usr/lol"'''
                       '''"Author and co"   Bot /usr/lol'''
                       '''"Author and co" Bot     "/usr/lol"'''
                       '''"Author and co"      'Bot' /usr/lol'''
                       '''Author   Bot     /usr/lol'''
                       '''  '   '   a   '   '  ''')

    def test_tournament(self):
        ID = 1
        self.tournament = Tournament(config_helpers.players_parse(os.path.join(GAME_PATH,
                                     config.players_config)), ID)

        print(__file__ + ":" + str(getframeinfo(currentframe())[1]))
        self.tournament.run()
        print(MAIN_MOCK.call_args_list)
        # print (sys.modules, file=open('log.txt', 'w'))
        # controller = self._simulator.play()
        # self.assertTrue(controller.is_finished)

if __name__ == '__main__':
    unittest.main()
