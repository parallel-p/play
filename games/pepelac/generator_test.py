import unittest
import unittest.mock
mock = unittest.mock.Mock()
r_mock = unittest.mock.Mock()
r_mock.randint.side_effect = [i for i in range(50)]
import generator


_field_size = 50


class GeneratorTest(unittest.TestCase):
    def setUp(self):
        self.field = [[0 for i in range(_field_size)]
                      for j in range(_field_size)]
        self.players = ["bla-bla" for i in range(4)]
        self.players_count = 2
        self.bullets_count = self.players_count * 2
        self.gen = generator.Generator()

    def test_generate_players(self):
        new_field = self.gen.generate_players(self.field, self.players_count)
        sum = 0
        for i in new_field:
            for j in i:
                sum += j
        self.assertEqual(sum, 3)

    def test_generate_bullets(self):
        new_field = self.gen.generate_bullets(self.field,
                                              self.bullets_count)
        sum = 0
        for i in new_field:
            for j in i:
                sum += j
        self.assertEqual(sum, -4)

if __name__ == '__main__':
    unittest.main()
