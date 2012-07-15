import random
import unittest
from unittest.mock import Mock
from game_master import GameMaster
from generator import Generator


class GameMasterTests(unittest.TestCase):
    def setUp(self):
        players = [Mock(name='player 0'), Mock(name='player 1')]
        generator = Generator()
        start_states = list(
            generator.generate_start_positions(Mock(), players)
        )
        self._start_state = random.choice(start_states)
        self._simulator = self._get_simulator(players)
        self._master = GameMaster(self._simulator, self._start_state)
        self._states = []

    def test_game_master(self):
        while not self._simulator.is_finished:
#            if(len(self._states)>0):
#                print("start "+str(self._states[-1]))
            self._master.tick(self._start_state)
#            self._start_state = self._states[-1]
#            print(self._simulator._states)

#        scores = self._simulator.get_scores()
#        print(scores)
#        scores_values = list(scores.values())
#        players = self._simulator.get_players()
#        self.assertEqual(set(players), set(scores.keys()))
#        print(scores)

    def _get_simulator(self, players):
        simulator = Mock()
        simulator._states = []
        simulator._scores = None
        simulator.get_players.return_value = players
        simulator.get_states.return_value = simulator._states
        simulator.get_scores.side_effect = lambda: simulator._scores
        simulator.is_finished = False

        def report_state(state):
            simulator._states.append(state)

        def get_move(player, state, serialize, deserialize):
            return (0, 0)

        def finish_game(scores):
            simulator._scores = scores
            simulator.is_finished = True

        simulator.report_state.side_effect = report_state
        simulator.get_move.side_effect = get_move
        simulator.finish_game.side_effect = finish_game
        return simulator

if __name__ == '__main__':
    unittest.main()
