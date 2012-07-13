import unittest
import config_helpers
import imp
import os


class TestConfigHelpers(unittest.TestCase):
    def setUp(self):
        os.chdir('..')
        conf_file = open('config.py', 'w')
        conf_file.write('some_value = 0\n')
        conf_file.close()

    def test_initialize_game_environment(self):
        config_helpers.initialize_game_environment('config.py')
        import config
        self.assertEqual(config.some_value, 0)


class GameTest(unittest.TestCase):

    def test_write_logs(self):
        list = config_helpers.players_parse('test_for_players_parse')
        for l in list:
            print(l)


if __name__ == '__main__':
    unittest.main()
