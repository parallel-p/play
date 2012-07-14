import unittest
import game_controller
from player import Player
from tournament_stages.game_supporting_classes import GameSignature  # ?

class PlayerState:
    def __init__(self, _a):
        self.a = _a

class Config:
    def __init__(self):
        self.real_time_limit_seconds = 1
        self.memory_limit_mb = 64
        self.cpu_time_limit_seconds = 1

def deserialize(stream):
    return stream.readline().decode('utf-8')

def serialize(player_state, stream):
    stream.write(bytes(player_state.a, 'utf-8'))
    stream.write(b'\n')

'''
TODO:
    Fix constructor parameters
'''
config = Config()
players = [Player('python IntegrationBot.py', 'IntegrationTest', 'IntegrationBot')]
signature = GameSignature(1, 2, 3, 4)
jury_state = None


class IntegrationTest(unittest.TestCase):
    def test_controller(self):
        game = game_controller.GameController(config, players,
                                              signature, jury_state)
        game.create_bots()
        ps = PlayerState('42')
        move = game.get_move(players[0], ps, serialize, deserialize)
        game.kill_bots()
        self.assertEqual(move, '42\n')


if __name__ == '__main__':
    unittest.main()
