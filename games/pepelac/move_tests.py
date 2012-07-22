import unittest
import io
from move import deserialize_move, DeserializeMoveException


class MoveTests(unittest.TestCase):
    def test_deserialization(self):
        stream = io.BytesIO(b'STAND\nDOWN\n')
        move = deserialize_move(stream)
        self.assertEqual(move[0], 0)
        self.assertEqual(move[1], 0)
        move = deserialize_move(stream)
        self.assertEqual(move[0], 1)
        self.assertEqual(move[1], 0)

    def test_error_raising(self):
        stream = io.BytesIO(b'SOMETHING--Odd')
        with self.assertRaises(DeserializeMoveException):
            move = deserialize_move(stream)


if __name__ == '__main__':
    unittest.main()
