import unittest
from unittest.mock import Mock, patch
with patch.dict('sys.modules',
                {'config': Mock(), 'tournament_systems': Mock()}):
    import config
    import tournament_systems as all_ts
    import tournament_system_factory as ts_factory


class TS1:
    pass


class TS2:
    pass


class TournamentSystemFactoryTests(unittest.TestCase):
    def setUp(self):
        all_ts.tournament_systems = {"ts1": TS1, "ts2": TS2}

    def test_all_tournament_systems(self):
        for ts_name, ts in all_ts.tournament_systems.items():
            config.tournament_system = ts_name
            self.assertTrue(isinstance(
                ts_factory.TournamentSystemFactory().create(), ts
            ))

    def test_exception_no_tournament_system(self):
        config.tournament_system = ""
        with self.assertRaises(ts_factory.TournamentSystemNotFoundException):
            ts_factory.TournamentSystemFactory().create()

    def test_exception_not_available_tournament_system(self):
        config.tournament_system = "abacaba"
        with self.assertRaises(ts_factory.TournamentSystemNotFoundException):
            ts_factory.TournamentSystemFactory().create()

if __name__ == '__main__':
    unittest.main()
