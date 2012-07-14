import unittest
from unittest.mock import MagicMock, Mock, patch
import sys
with patch.dict('sys.modules', {'config_helpers': MagicMock(),
                                'config': MagicMock(),
                                'tournament_stages.tournament': MagicMock(),
                                'Tournament': MagicMock()}):
    import config
    import config_helpers
    from tournament_stages.tournament import Tournament
    import main


class MainTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_functions(self):
        self.main = main.Main('Ata dir', 1)
        self.main.load_config()
        self.main.load_players()
        Tournament().get_results.return_value='First player won'
        self.main.run_tournament()
        if self.main.show_result() != 'First player won':
            raise Exception("main.py doesn't work")

    def test_main(self):
        self.main = main.Main('Ata dir', 1)
        Tournament().get_results.return_value='First player won'
        self.main.main()
        if self.main.show_result() != 'First player won':
            raise Exception("main.py doesn't work")

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
