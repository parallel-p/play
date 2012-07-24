import unittest
import io
from move import deserialize


class MoveTests(unittest.TestCase):
    def test_deserialization(self):
        stream = io.BytesIO(b'1 1\n1 100')
        move = deserialize(stream)
        self.assertEqual(move[0], 1)
        self.assertEqual(move[1], 1)
        move = deserialize(stream)
        self.assertEqual(move[0], 1)
        self.assertEqual(move[1], 100)

if __name__ == '__main__':
    unittest.main()
