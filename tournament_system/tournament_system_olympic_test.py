import tournament_system_olympic
import unittest
from unittest.mock import Mock


PLAYERS_LIST = [1, 2, 3, 4, 5, 6, 7, 8]
FIRST = {1: {1: 0, 2: 5}, 2: {3: 7, 4: 0}, 3: {5: 8, 6: 4}, 4: {7: 2, 8: 1}}
SECOND = {5: {2: 9, 3: 1}, 6: {5: 8, 7: 1}}
THIRD = {7: {2: 4, 5: 7}}
FIRST_ROUND = [[1, 2], [3, 4], [5, 6], [7, 8]]
SECOND_ROUND = [[2, 3], [5, 7]]
THIRD_ROUND = [[2, 5]]
CONFIG_DATA = ''


class TournamentSystemOlympicTest(unittest.TestCase):
    def test_get_rounds(self):
        test_rounds = \
            tournament_system_olympic.TournamentSystemOlympic(PLAYERS_LIST,
                                                              CONFIG_DATA)
        test_rounds.get_current_round_results = Mock()
        test_rounds.get_current_round_results.side_effect = \
                [FIRST, SECOND, THIRD]
        list_of_rounds = list(test_rounds.get_rounds())
        first_players = list(list_of_rounds[0])
        second_players = list(list_of_rounds[1])
        third_players = list(list_of_rounds[2])
        self.assertEqual(first_players, FIRST_ROUND)
        self.assertEqual(second_players, SECOND_ROUND)
        self.assertEqual(third_players, THIRD_ROUND)

if __name__ == '__main__':
    unittest.main()
