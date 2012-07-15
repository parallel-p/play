from tournament_systems.tournament_system_each import TournamentSystemEach
import unittest

PLAYERS_LIST = [1, 2]
ANSWER = [[[1, 2]]]
CONFIG = []
RESULTS = {1: {1: 10, 2: 179}}


class TournamentSystemEachTest(unittest.TestCase):
    def test_get_rounds(self):
        ts = TournamentSystemEach(PLAYERS_LIST)
        self.assertEqual(list(ts.get_rounds()), ANSWER)

    def test_get_table(self):
        #For newline
        print()
        ts = TournamentSystemEach(PLAYERS_LIST)
        ts.add_round_results(RESULTS)
        table = ts.get_table()
        for string in table:
            print(string)


if __name__ == "__main__":
    unittest.main()
