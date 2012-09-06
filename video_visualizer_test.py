import unittest
from unittest.mock import Mock, MagicMock
from random import randint, randrange
import visualizer
import os
import subprocess
import pickle
import shutil
from tournament_stages.game_signature import GameSignature
from player import Player


# Unfortunately, Mock objects cannot be pickled, so we have to do like this:
class GameControllerMock:
    def __init__(self):
        self.jury_states = []
        self._players = [Player(None, 'Dmitry Tomp'),
                         Player(None, 'Daniil Ryazanovsky'),
                         Player(None, 'Alex Dmitriev')]
        self.signature = GameSignature()

    def __lt__(self, other):
        return self.signature < other.signature


class VideoVisualizerIntegrationTest(unittest.TestCase):
    def setUp(self):
        if os.path.exists('test'):
            shutil.rmtree('test')
        os.mkdir('test')
        os.chdir('test')

        # For mocking a paint funtion:
        def side_effect(self, fname):
            f = open(os.path.join('images', fname), 'rb')
            retv = f.read()
            f.close()
            return retv

        # There should be an image folder containing png images with specified
        # names (see below).
        self.painter_obj = Mock
        self.painter_obj.paint = side_effect

    def test_compile(self):
        # Generate many random GameControllers.
        gc = GameControllerMock()
        for gc.signature.tournament_id in range(randint(1, 3)):
            for gc.signature.round_id in range(randint(1, 3)):
                for gc.signature.series_id in range(randint(1, 3)):
                    for gc.signature.game_id in range(randint(1, 3)):
                        filenum = 0
                        gc.jury_states = [str(randrange(19) + 1).zfill(2) + '.'
                                          'png' for i in range(randint(3, 20))]
                        while os.path.exists('contr' + str(filenum) + '.gc'):
                            filenum = randrange(10000000000)
                        with open('contr' + str(filenum) + '.gc', 'wb') as f:
                            pickle.dump(gc, f)
        os.chdir('..')
        if os.path.exists(os.path.join('test', 'result.avi')):
            os.remove(os.path.join('test', 'result.avi'))

        visualizer.VideoVisualizer(
            3, self.painter_obj, '*.gc', 'test'
        ).compile('result.avi')

        # Check whether all images have been removed:
        for fname in os.listdir('test'):
            self.assertTrue(fname.endswith('.gc') or fname == 'result.avi')

    def tearDown(self):
        # To be able to watch the resulting video file manually, let's copy it.
        if os.path.exists(os.path.join('test', 'result.avi')):
            shutil.copyfile(os.path.join('test', 'result.avi'), 'result.avi')
        shutil.rmtree('test')


if __name__ == '__main__':
    unittest.main()
