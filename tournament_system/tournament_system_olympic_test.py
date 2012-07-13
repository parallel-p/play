import tournament_system_olimpic
import unittest
from unittest.mock import Mock


PLAYERS_LIST = [1, 2, 3, 4, 5, 6, 7, 8]
RESULTS = {1: {1:2, 2:0}, }
CONFIG_DATA = ''


class TournamentSystemOlimpicTest(unittest.TestCase):
    def test_get_rounds(self):
        test_rounds = \
            tournament_system_olimpic.TournamentSystemOlimpic(PLAYERS_LIST,
                                                              CONFIG_DATA)
        test_rounds.get_rounds()
        tmp = test_rounds.get_all_results()
        #self.assertEqual(test_answer, ANSWER)
        print(tmp)


if __name__ == '__main__':
    unittest.main()
