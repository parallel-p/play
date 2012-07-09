import player
import unittest
from unittest.mock import Mock


PLAYER_COMMAND = 'python3 test_game.py'
WRONG_PLAYER_COMMAND = 'fffaaasd test_game.py'


class PlayerTest(unittest.TestCase):
    def test_create_process(self):
        test_player = player.Player(PLAYER_COMMAND)
        test_player.create_process()
        self.assertTrue(test_player._is_running())
        test_player.kill_process()

    def test_wrong_command(self):
        test_player = player.Player(WRONG_PLAYER_COMMAND)
        with self.assertRaises(OSError):
            test_player.create_process()

    def test_kill_process(self):
        test_player = player.Player(PLAYER_COMMAND)
        test_player.create_process()
        test_player.kill_process()
        self.assertFalse(test_player._is_running())

    def test_get_move(self):
        def side_effect_for_deserialize(pipe):
            self.assertEqual(b'abc\n', pipe.readline())

        def side_effect_for_serialize(pipe):
            pipe.write(b'abc\n')

        test_player = player.Player(PLAYER_COMMAND)
        test_player.create_process()

        move = Mock()
        move.deserialize()
        move.deserialize.side_effect = side_effect_for_deserialize

        player_state = Mock()
        player_state.serialize()
        player_state.serialize.side_effect = side_effect_for_serialize

        test_player.get_move(player_state, move)
        self.assertTrue(move.deserialize.called)
        self.assertTrue(player_state.serialize.called)
        test_player.kill_process()

if __name__ == '__main__':
    unittest.main()
