from PIL import Image, ImageTk
import unittest as ut
from unittest.mock import Mock, MagicMock, patch
from os.path import join
import frame_visualizer
from os import listdir as ls
import config

imgpath = '../images'
# See tests with or without byte streaming


def paint_image(jury_state):
    ''' Opens an image file and returns an ``Image`` object.
    Used for testing user interface. '''
    return Image.open(join(imgpath, jury_state))


def paint_bytes(jury_state):
    ''' Opens an image file and returns a byte stream.
    Used for checking bytestream->Image conversion. '''
    return open(join(imgpath, jury_state), mode="rb").read()


def do_nothing(image):
    ''' Fake bytestream->Image conversion. Used to mock the
    real one for testing with ``paint_image``. '''
    return image


class FrameVisualizerTestCase(ut.TestCase):


    def test_without_byte_streaming(self):
        ''' This test checks user interface. It opens some images in
        ../images directory and passes them directly to the visualizer. '''
        print("TEST WITHOUT BYTE STREAMING")
        game_controller = Mock()
        game_controller.jury_states = sorted(ls(path=imgpath))
        frame_visualizer._bytes2image = Mock(side_effect=do_nothing)
        vis = frame_visualizer.FrameVisualizer(game_controller)
        painter = Mock()
        painter.paint = Mock(side_effect=paint_image)
        vis.painter_factory = Mock(return_value=painter)
        vis.mainloop()

    def test_with_byte_streaming(self):
        ''' This test checks bytestream->Image conversion.
        Painter is mocked here, and the visualizer will draw
        images from ../images directory. If images aren't
        corrupted during conversion, you will see numbers
        from 1 to 20 in the GUI. '''
        print("TEST WITH BYTE STREAM")
        game_controller = Mock()
        game_controller.jury_states = sorted(ls(path=imgpath))
        vis = frame_visualizer.FrameVisualizer(game_controller)
        painter = Mock()
        painter.paint = Mock(side_effect=paint_bytes)
        vis.painter_factory = Mock(return_value=painter)
        vis.mainloop()


    def test_with_nim_painter(self):
        ''' This is a complete test with painter of 'example nim'.
        If everything is OK, three heaps with n, n + 1 and n + 2
        (where 0 <= n < 10) stones will be shown. 
        This test has no mocks in ``frame_visualizer`` module
        and is the most close to real game. '''
        print('TESTING WITH NIM PAINTER')
        game_controller = Mock()
        game_controller.jury_states = []
        for i in range(10):
            game_controller.jury_states.append(
                config.JuryState([i, i + 1, i + 2]))
                # A JuryState in this game consists of two enumerations:
                # first of them contains players (painter doesn't need them)
                # and the second one has numbers of stones in each heap.
        vis = frame_visualizer.FrameVisualizer(game_controller)
        vis.mainloop()


if __name__ == '__main__':
    ut.main()
