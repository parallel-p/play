import sys

GAME_PATH = 'games/pepelac'
BOTS = [sys.executable + ' games/nim/bots/random_bot.py',
        sys.executable + ' games/nim/bots/wrong_bot.py']

import config_helpers
config_helpers.initialize_game_environment(GAME_PATH)
import config
import bot
import unittest
import time
import psutil
from unittest.mock import Mock
from bot import TimeLimitException


PLAYER_COMMAND = sys.executable + ' test_game.py'
ML_PLAYER_COMMAND = sys.executable + ' test_game2.py'
WRONG_PLAYER_COMMAND = 'fffaaasd test_game.py'
PLAYER_STATE = ''
CONFIG = Mock()
# check 'time_limit' every 'frequency_of_inspection_time' moves
CONFIG.real_time_limit_seconds = 5.0
CONFIG.cpu_time_limit_seconds = 10.0
CONFIG.memory_limit_mb = 15.0
CONFIG.frequency_of_inspection_time = 1000
TIME = CONFIG.real_time_limit_seconds
MEMORY = CONFIG.memory_limit_mb
NORMAL_TIME = TIME / 5


class BotTest(unittest.TestCase):
    def test_create_process(self):
        ''' This test checks if bot process are created correctly. '''
        test_bot = bot.Bot(PLAYER_COMMAND)
        test_bot.create_process()
        self.assertTrue(test_bot._process.is_running())
        test_bot.kill_process()

    def test_wrong_command(self):
        ''' This test checks whether error is raised when wrong
        command is executed '''
        test_bot = bot.Bot(WRONG_PLAYER_COMMAND)
        with self.assertRaises(OSError):
            test_bot.create_process()

    def test_kill_process(self):
        ''' This test checks if the bot process was killed correctly '''
        test_bot = bot.Bot(PLAYER_COMMAND)
        test_bot.create_process()
        test_bot.kill_process()
        self.assertFalse(test_bot._process.is_running())

    def test_get_move(self):
        ''' This test checks whether bot's IO is working properly '''
        def side_effect_for_deserialize(pipe):
            self.assertEqual(b'abc\n', pipe.readline())

        def side_effect_for_serialize(PLAYER_STATE, pipe):
            pipe.write(b'abc\n')

        test_bot = bot.Bot(PLAYER_COMMAND)
        test_bot.create_process()

        deserialize = Mock()
        deserialize().side_effect = side_effect_for_deserialize

        serialize = Mock()
        serialize().side_effect = side_effect_for_serialize

        move = test_bot.get_move(PLAYER_STATE, serialize, deserialize)
        self.assertTrue(serialize.called)
        self.assertTrue(deserialize.called)
        test_bot.kill_process()

    def test_time_error(self):
        ''' This test checks if a ``TimeLimitError`` is raised when
        a bot exceeds time limit and whether it isn't raised if not. '''
        def side_effect_for_deserialize(timeout):
            time.sleep(timeout)

        def side_effect_for_serialize(PLAYER_STATE, timeout):
            time.sleep(timeout)

        def test_without_timelimit_error():
            deserialize.side_effect = side_effect_for_deserialize(NORMAL_TIME)
            serialize.side_effect = \
                side_effect_for_serialize(PLAYER_STATE, NORMAL_TIME)
            test_bot.create_process()
            clock_time = time.clock()
            move = test_bot.get_move(PLAYER_STATE, serialize, deserialize)
            test_bot.kill_process()
            self.assertLessEqual(time.clock(), clock_time + TIME)

        def test_with_timelimit_error():
            deserialize.side_effect = side_effect_for_deserialize(TIME)
            serialize.side_effect = side_effect_for_serialize(PLAYER_STATE,
                                                              TIME)
            test_bot.create_process()
            move = test_bot.get_move(PLAYER_STATE, serialize, deserialize)
            self.assertRaises(TimeLimitException)
            test_bot.kill_process()

        test_bot = bot.Bot(PLAYER_COMMAND)
        deserialize = Mock()
        serialize = Mock()
        test_without_timelimit_error()
        test_with_timelimit_error()

if __name__ == '__main__':
    unittest.main()
