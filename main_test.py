import os
import unittest
from unittest.mock import MagicMock, patch
from exceptions import PlayersException

with patch.dict('sys.modules',
                {'config_helpers': MagicMock(),
                 'config': MagicMock(),
                 'Tournament': MagicMock(),
                 '_load_players': MagicMock(),
                 'print_tournament_system_results': MagicMock()}):
    import main


class MainTest(unittest.TestCase):

    def setUp(self):
        self.main = main.Main('game_path', 42)
        main.config_helpers = MagicMock()
        main.config = MagicMock()
        main.Tournament = MagicMock()

    def test_init(self):
        self.assertEqual(self.main._game_path, 'game_path')
        self.assertEqual(self.main._tournament_id, 42)

    def test_load_players(self):
        main.config_helpers.players_parse.return_value = [1, 2, 3]
        main.config.players_config = '42'
        self.main._load_players()
        self.assertEqual(self.main._players_list, [1, 2, 3])
        main.config_helpers.players_parse.return_value = None
        try:
            self.main._load_players()
        except PlayersException:
            return
        else:
            raise Exception('Test of _load_players failed')

    def test_run_tournament_and_show_result(self):
        main.Tournament().get_results.return_value = 42
        main.Tournament().run = MagicMock()
        self.main._run_tournament()
        self.assertEqual(self.main.tournament_results, 42)
        self.assertEqual(self.main.show_result(), 42)
        main.Tournament().run.assert_called_once_with()

    def test_print_tournament_system_results(self):
        main.print_tournament_system_results = MagicMock()
        self.main._print_tournament_results(42)
        main.print_tournament_system_results.assert_called_once_with(42)

    def test_get_free_dirname(self):
        if self.main._get_free_dirname('logs',
                                       'tournament') not in range(1, 1024):
            raise Exception('_get_free_dirname doesn\'t work')

    def test_make_good_tournament_id(self):
        self.main._tournament_id = None
        self.main._make_good_tournament_id()
        self.assertNotEqual(self.main._tournament_id, None)
        self.main._tournament_id = 42
        self.main._make_good_tournament_id()
        self.assertEqual(self.main._tournament_id, 42)

    def test_main(self):
        main.bot = MagicMock()
        self.main._load_players = MagicMock()
        self.main._make_good_tournament_id = MagicMock()
        self.main._run_tournament = MagicMock()
        self.main._print_tournament_results = MagicMock()
        self.main.tournament = MagicMock()
        self.main.tournament.tournament_system = MagicMock()
        self.main.main()
        self.main._load_players.assert_called_once_with()
        self.main._make_good_tournament_id.assert_called_once_with()
        self.main._run_tournament.assert_called_once_with()
        self.main._print_tournament_results.assert_called_once_with(\
            self.main.tournament.tournament_system)


if __name__ == '__main__':
    unittest.main()
