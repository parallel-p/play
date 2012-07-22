from PIL import Image
import unittest
from unittest.mock import Mock
import os
from os import listdir as ls
import development_tools.frame_visualizer as frame_visualizer

imgpath = '../images'
# See tests with or without byte streaming


def paint_image(jury_state):
    ''' Opens an image file and returns an ``Image`` object.
    Used for testing user interface. '''
    return Image.open(os.path.join(imgpath, jury_state))


def paint_bytes(jury_state):
    ''' Opens an image file and returns a byte stream.
    Used for checking bytestream->Image conversion. '''
    return open(os.path.join(imgpath, jury_state), mode="rb").read()


def do_nothing(image):
    ''' Fake bytestream->Image conversion. Used to mock the
    real one for testing with ``paint_image``. '''
    return image


class FrameVisualizerTestCase(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
