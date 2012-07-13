import random
import unittest
from unittest.mock import Mock
from game_master import GameMaster
from generator import Generator


class GameMasterTests(unittest.TestCase):
    def setUp(self):
        players = [Mock(name='player 0'), Mock(name='player 1')]
        generator = Generator()
        start_states = list(generator.generate_start_positions(Mock(), 2))
        self._start_state = random.choice(start_states)
        self._controller = self._get_controller(players)
        self._master = GameMaster(self._controller, self._start_state)

    def test_that_in_the_end_of_the_game_we_have_empty_heaps(self):
        self._master.tick(self._start_state)
        last_state = self._controller.get_states()[-1]
        empty_heap_sizes = [0] * len(last_state.heap_sizes)
        self.assertEqual(last_state.heap_sizes, empty_heap_sizes)

    def test_that_only_one_player_wins(self):
        self._master.tick(self._start_state)
        scores = self._controller.get_scores()
        scores_values = list(scores.values())
        players = self._controller.get_players()
        self.assertEqual(set(players), set(scores.keys()))
        self.assertTrue(scores_values == [0, 1] or scores_values == [1, 0])

    def _get_controller(self, players):
        controller = Mock()
        controller._states = []
        controller._scores = None
        controller.get_players.return_value = players
        controller.get_states.return_value = controller._states
        controller.get_scores.side_effect = lambda: controller._scores

        def report_state(state):
            controller._states.append(state)

        def get_move(player, heap_sizes, serialize, deserialize):
            allowed = [i for i, size in enumerate(heap_sizes)
                       if size > 0]
            heap_number = random.choice(allowed)
            removed_stones = random.randint(1, heap_sizes[heap_number])
            return (heap_number, removed_stones)

        def finish_game(scores):
            controller._scores = scores

        controller.report_state.side_effect = report_state
        controller.get_move.side_effect = get_move
        controller.finish_game.side_effect = finish_game
        return controller

if __name__ == '__main__':
    unittest.main()
