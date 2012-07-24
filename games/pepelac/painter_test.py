from painter import Painter
from PIL import Image
import unittest
from unittest.mock import Mock
import random
from os.path import dirname, join
import os
import painter as painter_module

MYDIR = dirname(__file__)

class PainterTests(unittest.TestCase):

    def setUp(self):
        self.imgpath = join(MYDIR, 'images')
        player1 = Mock(author_name='Vasya', bot_name='Razor', cmd_line='')
        player2 = Mock(author_name='Petya', bot_name='Vizor', cmd_line='')
        player3 = Mock(author_name='Igor', bot_name='Dead', cmd_line='')

        field = [[0, 2, -1], [1, -1, -1], [-1, -1, -1]]
        self.jury_states = [Mock(field=field,
            field_side=3,
            bullets=[0, 0, 0],
            explosion_time=10,
            dead_players=[player3],
            dead_reasons={player3: 'X'},
            collision=None,
            scores={player3: 1}),
            Mock(field=field,
                field_side=3,
                bullets=[0, 0, 0],
                explsion_time=10,
                dead_players=[player3],
                dead_reasons={player3: 0},
                collision=None,
                scores={player3: 1}),
            Mock(field=field,
                field_side=3,
                bullets=[0, 0, 0],
                explosion_time=10,
                dead_players=[player3],
                dead_reasons={player3: 1},
                collision=None,
                scores={player3: 1})]

        self.players = [player1, player2, player3]
        self.painter_object = painter_module.Painter(self.players)

    def test__resize(self):
        for i in os.listdir(self.imgpath):
            image = painter_module.image_resize(join(self.imgpath, i), 10)
            self.assertLessEqual(image.size[0], 10)
            self.assertLessEqual(image.size[1], 10)

    def test_creation(self):
        self.assertEqual(self.players, self.painter_object.players)

    def test__initialize(self):
        for js in self.jury_states:
            self.painter_object._initialize(js)
            self.assertEqual(
                512 // js.field_side, self.painter_object._cell_side)
            self.assertTrue(self.painter_object._is_initialized)
            self.assertEqual(self.painter_object._width, 1586)
            self.assertEqual(self.painter_object._height, 512)
            self.assertTrue(
                hasattr(self.painter_object, '_fire_ico') and (
                hasattr(self.painter_object, '_patron_ico')) and (
                hasattr(self.painter_object, '_player_ico')) and (
                hasattr(self.painter_object, '_player_ico_fight')) and (
                hasattr(self.painter_object, '_patron_ico_fight')) and (
                hasattr(self.painter_object, '_patron_ico_left')))

    def test_dead_reason(self):
        mydict = {
            self.jury_states[0]: 'Death reason: X',
            self.jury_states[1]: 'Death reason: killed by armageddon',
            self.jury_states[2]: 'Death reason: killed by other player'
            }
        for i in mydict.keys():
            self.assertEqual(self.painter_object.dead_reason(
                i, self.players[2]), mydict[i])

    def test_cut_name(self):
        self.assertEqual('abc', self.painter_object.cut_name('abc'))
        self.assertEqual(
            'abcabcabcabc...',
             self.painter_object.cut_name('abcabcabcabcabca'))


    def test_index_of_player(self):
        self.assertEqual(-1, self.painter_object.index_of_player([], None))
        self.assertEqual(
            -1,
            self.painter_object.index_of_player([
                self.players[0],
                self.players[1]],
                self.players[2]))
        self.assertEqual(0, self.painter_object.index_of_player(
            self.players, self.players[0]))

    def test_paint(self):
        for js in self.jury_states:
            self.assertTrue(isinstance(self.painter_object.paint(js), bytes))


if __name__ == '__main__':
    unittest.main()
