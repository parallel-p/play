import bot
import unittest
import time
import psutil
from unittest.mock import Mock
from bot import TimeLimitException, MemoryLimitException


PLAYER_COMMAND = 'python3 test_game.py'
ML_PLAYER_COMMAND = 'python3 test_game2.py'
WRONG_PLAYER_COMMAND = 'fffaaasd test_game.py'

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
        test_bot = bot.Bot(PLAYER_COMMAND, CONFIG)
        test_bot.create_process()
        self.assertTrue(test_bot._is_running())
        test_bot.kill_process()

    def test_wrong_command(self):
        test_bot = bot.Bot(WRONG_PLAYER_COMMAND, CONFIG)
        with self.assertRaises(OSError):
            test_bot.create_process()

    def test_kill_process(self):
        test_bot = bot.Bot(PLAYER_COMMAND, CONFIG)
        test_bot.create_process()
        test_bot.kill_process()
        self.assertFalse(test_bot._is_running())

    def test_get_move(self):
        def side_effect_for_deserialize(pipe):
            self.assertEqual(b'abc\n', pipe.readline())

        def side_effect_for_serialize(pipe):
            pipe.write(b'abc\n')

        test_bot = bot.Bot(PLAYER_COMMAND, CONFIG)
        test_bot.create_process()

        move = Mock()
        move.deserialize()
        move.deserialize.side_effect = side_effect_for_deserialize

        player_state = Mock()
        player_state.serialize()
        player_state.serialize.side_effect = side_effect_for_serialize

        test_bot.get_move(player_state, move)
        self.assertTrue(move.deserialize.called)
        self.assertTrue(player_state.serialize.called)
        test_bot.kill_process()

    def test_time_error(self):
        def side_effect_for_deserialize(timeout):
            time.sleep(timeout)

        def side_effect_for_serialize(timeout):
            time.sleep(timeout)

        def test_without_timelimit_error():
            move.deserialize.side_effect = \
                                    side_effect_for_deserialize(NORMAL_TIME)
            player_state.serialize.side_effect = \
                                    side_effect_for_serialize(NORMAL_TIME)
            test_bot.create_process()
            clock_time = time.clock()
            test_bot.get_move(player_state, move)
            test_bot.kill_process()
            self.assertLessEqual(time.clock(), clock_time + TIME)

        def test_with_timelimit_error():
            move.deserialize.side_effect = \
                                    side_effect_for_deserialize(TIME)
            player_state.serialize.side_effect = \
                                    side_effect_for_serialize(TIME)
            test_bot.create_process()
            test_bot.get_move(player_state, move)
            self.assertRaises(TimeLimitException)
            test_bot.kill_process()

        test_bot = bot.Bot(PLAYER_COMMAND, CONFIG)
        move = Mock()
        move.deserialize()

        player_state = Mock()
        player_state.serialize()

        test_without_timelimit_error()
        test_with_timelimit_error()

    def test_memory_error(self):
        def test_without_memorylimit_error():
            test_bot = bot.Bot(PLAYER_COMMAND, CONFIG)
            test_bot.create_process()
            test_bot.get_move(player_state, move)
            # megabyte = 2 ** 20
            cpu_memory = test_bot._process.get_memory_info().rss / (2 ** 20)
            test_bot.kill_process()
            self.assertLessEqual(cpu_memory, MEMORY)

        def test_with_memorylimit_error():
            test_bot = bot.Bot(ML_PLAYER_COMMAND, CONFIG)
            test_bot.create_process()
            test_bot.get_move(player_state, move)
            self.assertRaises(MemoryLimitException)
            test_bot.kill_process()

        move = Mock()
        move.deserialize()

        player_state = Mock()
        player_state.serialize()

        test_without_memorylimit_error()
        test_with_memorylimit_error()

if __name__ == '__main__':
    unittest.main()
