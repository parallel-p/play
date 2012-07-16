import unittest
import os
import shutil
from tournament_stages.game_signature import GameSignature
from unittest.mock import MagicMock, patch
with patch.dict('sys.modules', {'engine': MagicMock(), 'jury_state': MagicMock(), 'config': MagicMock(), 'players': MagicMock()}):
    import jury_state
    import config
    import players
from tournament_stages.game import Game


class GameTest(unittest.TestCase):
    def test_write_logs(self):
        game = Game(jury_state.JS(), GameSignature(1, 1, 1, 1),
                    players)
        game._write_logs()

    def tearDown(self):
        path = os.path.dirname(__file__)
        path = os.path.join(path, 'logs')
        if (os.path.exists(path) == 1):
            shutil.rmtree(path)


if __name__ == '__main__':
    unittest.main()
