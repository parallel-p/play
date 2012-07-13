import unittest
import pickle
from game_supporting_classes import GameSignature
from unittest.mock import MagicMock, Mock, patch
with patch.dict('sys.modules', {'engine': MagicMock(), 'jury_state': MagicMock(), 'config': MagicMock(), 'players': MagicMock()}):
    import engine
    import jury_state
    import config
    import players
from game import Game


class GameTest(unittest.TestCase):

    def test_write_logs(self):
        game = Game(jury_state.JS(), GameSignature(1, 1, 1, 1), config, players)
        game._write_logs()

if __name__ == '__main__':
    unittest.main()

