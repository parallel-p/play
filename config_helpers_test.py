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

