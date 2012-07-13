import unittest
from unittest.mock import MagicMock, Mock, patch
with patch.dict('sys.modules', {'config_helpers': MagicMock(),
                                'config': MagicMock(),
                                'tournament': MagicMock()}):
    import config
    import config_helpers
    from tournament_stages import tournament
    import main


class MainTest(unittest.TestCase):

    def setUp(self):
        self.main = main.Main()

    def test_main(self):
        print("I'm starting work!")
        self.main.load_config()
        self.main.load_players()
        unittest.assertNotEqual(main.config, MagicMock())
        tournament.Tournament().get_results(return_value='First player won')
        self.main.run_tournament()
        print(self.main.show_result())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
