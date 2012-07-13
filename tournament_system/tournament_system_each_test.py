import tournament_system_each
import unittest
from unittest.mock import Mock

PLAYERS_LIST = [1, 2, 3, 4]
ANSWER = [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
CONFIG = []


class TournamentSystemEachTest(unittest.TestCase):
    def test_get_rounds(self):
        ts = tournament_system_each.TournamentSystemEach(PLAYERS_LIST,
                                                         CONFIG)
        self.assertEqual(list(ts.get_rounds()), ANSWER)


if __name__ == "__main__":
    unittest.main()
