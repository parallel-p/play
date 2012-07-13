import tournament_system_olimpic
import unittest
from unittest.mock import Mock


PLAYERS_LIST = [1, 2, 3, 4]
ANSWER = [[1, 2], [3, 4]]
CONFIG_DATA = ''


class TournamentSystemOlimpicTest(unittest.TestCase):
    def test_get_rounds(self):
        test_round = \
            tournament_system_olimpic.TournamentSystemOlimpic(PLAYERS_LIST,
                                                              CONFIG_DATA)
        test_answer = list(test_round.get_rounds())
        self.assertEqual(test_answer, ANSWER)


if __name__ == '__main__':
    unittest.main()
