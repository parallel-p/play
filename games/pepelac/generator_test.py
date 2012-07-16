import unittest
import unittest.mock
mock = unittest.mock.Mock()
r_mock = unittest.mock.Mock()
r_mock.randint.side_effect = [i for i in range(50)]
with unittest.mock.patch.dict(
    'sys.modules', {'jury_state': mock, 'random': r_mock}
):
    import generator
    import random

_field_size = 50


class GeneratorTest(unittest.TestCase):
    def setUp(self):
        self.field = [[0 for i in range(_field_size)]
                      for j in range(_field_size)]
        self.players = ["bla-bla" for i in range(4)]
        self.players_count = 4
        self.bullets_count = self.players_count * 2
        self.gen = generator.Generator()

    def test_generate_players(self):
        new_field = self.gen.generate_players(self.field, self.players_count)
        c = self.bullets_count * 2
        for player in range(self.players_count):
            self.assertEqual(new_field[c][c + 1], player + 1)
            c = c + 2

    def test_generate_bullets(self):
        new_field = self.gen.generate_bullets(self.field,
                                              self.bullets_count)
        c = 0
        for bullet in range(self.bullets_count):
            self.assertEqual(new_field[c][c + 1], -1)
            c = c + 2
if __name__ == '__main__':
    unittest.main()
