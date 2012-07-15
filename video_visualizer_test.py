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


class VideoVisualizerTest(unittest.TestCase):
    def setUp(self):
        if os.path.exists('test'):
            shutil.rmtree('test')
        os.mkdir('test')
        os.chdir('test')

        # For mocking a paint funtion:
        def side_effect(fname):
            f = open(os.path.join('images', fname), 'rb')
            retv = f.read()
            f.close()
            return retv

        # There should be an image folder containing GIF images with specified
        # names (see below).
        painter_obj = Mock()
        painter_obj.paint = side_effect

        self.viz = visualizer.VideoVisualizer(3, painter_obj, '.*\.gc', 'test')

    def test_collect_game_images_to_video(self):
        os.chdir('..')
        if os.path.exists(visualizer.TEMPFILE_NAME):
            os.remove(visualizer.TEMPFILE_NAME)

        self.viz.collect_game_images_to_video([str(randrange(19) + 1).zfill(2)
                                              + '.gif'
                                              for i in range(randint(3, 20))])

        self.assertTrue(os.path.exists(visualizer.TEMPFILE_NAME))
        self.assertEqual(len(os.listdir('test')), 0)

    def test_generate_tournament_status(self):
        os.chdir('..')
        if os.path.exists(visualizer.TEMPFILE_NAME_TITLE):
            os.remove(visualizer.TEMPFILE_NAME_TITLE)

        # The visualizer doesn't know the frame size as it wasn't given any
        # game frames.
        self.viz.size = (640, 480)
        self.viz.generate_tournament_status(GameControllerMock())

        self.assertTrue(os.path.exists(visualizer.TEMPFILE_NAME_TITLE))
        for fname in os.listdir('test'):
            self.assertTrue(fname.endswith('.gc'))

    def test_compile(self):
        # Generate many random GameControllers.
        gc = GameControllerMock()
        for gc.signature.tournament_id in range(randint(1, 3)):
            for gc.signature.round_id in range(randint(1, 3)):
                for gc.signature.series_id in range(randint(1, 3)):
                    for gc.signature.game_id in range(randint(1, 3)):
                        filenum = 0
                        gc.jury_states = [str(randrange(19) + 1).zfill(2) + '.'
                                          'gif' for i in range(randint(3, 20))]
                        while os.path.exists('contr' + str(filenum) + '.gc'):
                            filenum = randrange(10000000000)
                        with open('contr' + str(filenum) + '.gc', 'wb') as f:
                            pickle.dump(gc, f)
        os.chdir('..')
        if os.path.exists(visualizer.TEMPFILE_NAME):
            os.remove(visualizer.TEMPFILE_NAME)
        if os.path.exists(visualizer.TEMPFILE_NAME_TITLE):
            os.remove(visualizer.TEMPFILE_NAME_TITLE)
        if os.path.exists(os.path.join('test', 'result.avi')):
            os.remove(os.path.join('test', 'result.avi'))

        self.viz.compile('result.avi')

        self.assertFalse(os.path.exists(visualizer.TEMPFILE_NAME))
        self.assertFalse(os.path.exists(visualizer.TEMPFILE_NAME_TITLE))
        # Check whether all images have been removed:
        for fname in os.listdir('test'):
            self.assertTrue(fname.endswith('.gc') or fname == 'result.avi')

    def tearDown(self):
        # To be able to watch the resulting video file manually, let's copy it.
        if os.path.exists(os.path.join('test', 'result.avi')):
            shutil.copyfile(os.path.join('test', 'result.avi'), 'result.avi')
        if os.path.exists(visualizer.TEMPFILE_NAME):
            os.remove(visualizer.TEMPFILE_NAME)
        if os.path.exists(visualizer.TEMPFILE_NAME_TITLE):
            os.remove(visualizer.TEMPFILE_NAME_TITLE)
        shutil.rmtree('test')


if __name__ == '__main__':
    unittest.main()
