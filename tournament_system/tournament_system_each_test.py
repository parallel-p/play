import tournament_system_each
import unittest
from unittest.mock import Mock

PLAYERS_LIST = [1, 2]
ANSWER = [[1, 2]]
CONFIG = []
RESULTS = {1: {1: 1, 2: 0}}
WIDTH = 3


class TournamentSystemEachTest(unittest.TestCase):
    def test_get_rounds(self):
        ts = tournament_system_each.TournamentSystemEach(PLAYERS_LIST,
                                                         CONFIG)
        self.assertEqual(list(ts.get_rounds()), ANSWER)

    def test_get_table(self):
        #For newline
        print()
        ts = tournament_system_each.TournamentSystemEach(PLAYERS_LIST,
                                                         CONFIG)
        ts.add_round_results(RESULTS)
        for string in ts.get_table(WIDTH):
            print(string)


if __name__ == "__main__":
    unittest.main()
