import unittest
from unittest.mock import Mock, MagicMock
from random import randint, randrange
import visualizer
import os
import subprocess
import pickle
import shutil


class VideoVisualizerTest(unittest.TestCase):
    def setUp(self):

        def less_than(self, other):
            return [self.game_signature.tournament_id,
                    self.game_signature.round_id,
                    self.game_signature.series_id,
                    self.game_signature.game_id] < [
                    other.game_signature.tournament_id,
                    other.game_signature.round_id,
                    other.game_signature.series_id,
                    other.game_signature.game_id]

        GameController = MagicMock()
        GameController.__lt__ = less_than
        GameController.game_signature = MagicMock()

        if not os.path.exists('test'):
            os.mkdir('test')
        os.chdir('test')

        with GameController.game_signature as sign:
            for sign.tournament_id in range(randint(3,10)):
                for sign.round_id in range(randint(3,10)):
                    for sign.series_id in range(randint(3,10)):
                        for sign.game_id in range(randint(3,10)):
                            GameController.game_signature = sign
                            filenum = 0
                            GameController.jury_states = [str(randrange(19) + 1).zfill(2) + '.png' for i in range(randint(3,20))]
                            while os.path.exists('contr' + str(filenum) + '.gc'):
                                filenum = randrange(1000)
                            with open('contr' + str(filenum) + '.gc', 'wb') as f:
                                pickle.dump(GameController, f)

        os.chdir('..')

        painter_obj = Mock()
        painter_obj.paint = lambda x: open(os.path.join('images', x), 'rb').read()

    def test_collect_game_images_to_video(self):
        pass

    def test_compile(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
