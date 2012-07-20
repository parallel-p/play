import unittest
import io
from move import deserialize


class MoveTests(unittest.TestCase):
    def test_deserialization(self):
        stream = io.BytesIO(b'1 2\n3 3')
        move = deserialize(stream)
        self.assertEqual(move[0], 1)
        self.assertEqual(move[1], 2)
        move = deserialize(stream)
        self.assertEqual(move[0], 3)
        self.assertEqual(move[1], 3)

if __name__ == '__main__':
    unittest.main()
