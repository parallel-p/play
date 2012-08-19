from jury_state import JuryState
from painter import Painter
from player import Player
import unittest
import random


class PainterTests(unittest.TestCase):
    def test_painter(self):
        field_side = 10
        empty_list = [0 for i in range(field_side)]
        empty_list_tuples = [(0, 0) for i in range(field_side)]
        empty_field = [empty_list for i in range(field_side)]
        empty_field_tuples = [empty_list_tuples for i in range(field_side)]
        jury_state = JuryState(field_side, [empty_field, empty_field],
                               [empty_field, empty_field],
                               [empty_field_tuples, empty_field_tuples])

        jury_state.fields[0] = [
                               [0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
                               [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                               [0, 0, -1, 2, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                               [0, 3, 3, 3, 0, 1, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 2, 2, 0, -1, 0, 0, 3, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 3, 0, 0],
                               [4, 4, 4, 4, 0, 0, 0, 3, 0, 0]]
        jury_state.start_fields[0] = [
                                     [0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
                                     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                                     [0, 0, 2, 2, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                     [0, 3, 3, 3, 0, 1, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 2, 2, 0, 0, 0, 0, 3, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 3, 0, 0],
                                     [4, 4, 4, 4, 0, 0, 0, 3, 0, 0]]
        jury_state.fields[1] = [
                               [0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
                               [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                               [0, 0, -1, 2, 0, 0, 0, 0, 0, 0],
                               [0, -1, 0, 0, 0, 0, 0, 0, 0, 1],
                               [0, 3, 3, 3, 0, 1, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 2, 2, 0, 0, 0, 0, 3, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 3, 0, 0],
                               [4, 4, 4, 4, 0, 0, 0, 3, 0, 0]]
        jury_state.start_fields[1] = [
                                     [0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
                                     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                                     [0, 0, 2, 2, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                     [0, 3, 3, 3, 0, 1, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 2, 2, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [4, 4, 4, 4, 0, 0, 0, 3, 3, 3]]

        jury_state.ships[0] = [[(1, 3)], [(2, 7)], [(4, 9)], [(5, 5)],
                               [(0, 8), (0, 9)], [(3, 2), (3, 3)],
                               [(7, 1), (7, 2)],
                               [(5, 1), (5, 2), (5, 3)],
                               [(7, 7), (8, 7), (9, 7)],
                               [(9, 0), (9, 1), (9, 2), (9, 3)]
                               ]
                                                                     
        jury_state.ships[1] = [[(1, 3)], [(2, 7)], [(4, 9)], [(5, 5)],
                               [(0, 8), (0, 9)], [(3, 2), (3, 3)],
                               [(7, 1), (7, 2)],
                               [(5, 1), (5, 2), (5, 3)],
                               [(9, 7), (9, 8), (9, 9)],
                               [(9, 0), (9, 1), (9, 2), (9, 3)]
                               ]

        #jury_state.winner = Player('c', 'Dmitry Philippov')
        current_painter = Painter([Player('c', 'Petya'),
                                   Player('c', 'Dmitry Philippov')]
                                  )
        byte_string = current_painter.paint(jury_state)

if __name__ == '__main__':
    unittest.main()
