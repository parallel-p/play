GAME_PATH = 'games/nim'
import config_helpers
config_helpers.initialize_game_environment(GAME_PATH)


import game_simulator
import unittest
import game_controller
from unittest.mock import Mock
import os
import player
from games.nim import generator
import subprocess

helloworld = '''
int main()
{
    return 0;
}
'''


class GameSimulatorTest(unittest.TestCase):
    def setUp(self):
        f = open('hello.cpp', 'w')
        f.writelines([helloworld])
        f.close()
        compile_string = ["g++", "hello.cpp"]
        subprocess.call(compile_string)

    def tearDown(self):
        if os.name == 'nt':
            os.remove('a.exe')
        else:
            os.remove('a.out')
        os.remove('hello.cpp')

    def test_game(self):
        def game_master_side_effect(game_controller, jury_state):
            game_master._game_controller = game_controller
            return game_master

        def game_side_effect(jury_state):
            game_master._game_controller.is_finished = True
        game_master = Mock()
        game_master.is_finished = False
        game_master.tick.side_effect = game_side_effect
        # Sample command line
        config = [player.Player('./a.out') for i in range(2)]
        gen = generator.Generator()
        start_state = next(gen.generate_start_positions(' ', 2))
        eng = game_simulator.GameSimulator(config, start_state, '')
        result = eng.play()
        game_master.tick.assert_called_once()

        answer = game_controller.GameController(config, [], start_state, eng)
        answer.is_finished = True
        self.assertEqual(answer.is_finished, result.is_finished)


if __name__ == '__main__':
    unittest.main()
