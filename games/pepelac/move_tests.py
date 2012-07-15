import unittest
import io
from move import deserialize, DeserializeMoveException


class MoveTests(unittest.TestCase):
    def test_deserialization(self):
        stream = io.BytesIO(b'Stand\nDown\nNothing\n')
        move = deserialize(stream)
        self.assertEqual(move[0], 0)
        self.assertEqual(move[1], 0)
        move = deserialize(stream)
        self.assertEqual(move[0], 1)
        self.assertEqual(move[1], 0)
        with self.assertRaises(DeserializeMoveException):
            move = deserialize(stream)
            

if __name__ == '__main__':
    unittest.main()
