import unittest as ut
from unittest.mock import Mock, patch
from os.path import dirname, join
import os
from io import BytesIO
import imghdr
from PIL import Image
import tkinter
import tempfile

MYDIR = os.path.dirname(__file__)

config_mock = Mock()
my_painter = Mock()

def paint_file(js):
    img = Image.open(join(MYDIR, '../images/0{}.gif'.format(js)))
    bytes = BytesIO()
    img.save(bytes, format='png')
    return bytes.getvalue()

my_painter.paint = Mock(side_effect=paint_file)
config_mock.Painter = Mock(return_value=my_painter)


with patch.dict('sys.modules', config=config_mock):
    import development_tools.frame_visualizer as vis_module

    class FrameVisualizerTestCase(ut.TestCase):
        def setUp(self):
            self.imgpath = join(MYDIR, '../images')
            self.game_controller = Mock()
            self.game_controller.jury_states = list(range(1, 10, 1))
            self.game_controller.get_players = Mock(return_value=[])
            self.vis_object = vis_module.FrameVisualizer(self.game_controller)
            tempfile._RandomNameSequence.__next__ = Mock(return_value='mocked')

        def test__bytes2image(self):
            for i in os.listdir(self.imgpath):
                print(i)
                file = open(join(self.imgpath, i), mode='rb')
                bytes = file.read()
                file.close()
                bytes2 = BytesIO()
                vis_module._bytes2image(bytes).save(
                    bytes2, format=imghdr.what(None, h=bytes))
                self.assertEqual(bytes, bytes2.getvalue())

        def test__resize(self):
            for i in os.listdir(self.imgpath):
                image = vis_module._resize(Image.open(join(self.imgpath, i)))
                self.assertLessEqual(image.size[0], 800)
                self.assertLessEqual(image.size[1], 600)

        def test_creation(self):
            self.assertEqual(
                self.vis_object.painter_factory, config_mock.Painter)
            self.assertEqual(self.vis_object.frame_number, 0)
            self.assertTrue(
                hasattr(self.vis_object, 'control_panel') and (
                    hasattr(self.vis_object, 'frame_label')))

        def test_control_panel__set_frame_number(self):
            self.vis_object.control_panel._set_frame_number(232)
            self.assertEqual(
                self.vis_object.control_panel.num_label['text'], 'Frame #233')

        def test_control_panel_creation(self):
            self.assertTrue(
                hasattr(self.vis_object.control_panel, 'back_button') and (
                    hasattr(
                        self.vis_object.control_panel, 'forward_button')) and (
                hasattr(self.vis_object.control_panel, 'num_label')))

        def test__back(self):
            self.vis_object._draw_frame = Mock()
            self.vis_object.frame_number = 0
            self.vis_object._back()
            self.assertEqual(self.vis_object._draw_frame.call_count, 0)
            self.vis_object.frame_number = 1
            self.vis_object._back()
            self.vis_object._draw_frame.assert_called_once_with(0)

        def test__forward(self):
            self.vis_object._draw_frame = Mock()
            self.vis_object.frame_number = len(
                self.game_controller.jury_states) - 1
            self.vis_object._forward()
            self.assertEqual(self.vis_object._draw_frame.call_count, 0)
            self.vis_object.frame_number = 0
            self.vis_object._forward()
            self.vis_object._draw_frame.assert_called_once_with(1)

        def test_mainloop(self):
            self.vis_object.pack = Mock()
            self.vis_object._draw_frame = Mock()
            tkinter.Frame.mainloop = Mock()

            self.vis_object.mainloop()

            self.vis_object.pack.assert_called_once_with()
            self.vis_object._draw_frame.assert_called_once_with(0)
            tkinter.Frame.mainloop.assert_called_once_with(self.vis_object)

    class FrameVisualizerDrawFrameTestCase(ut.TestCase):
        def setUp(self):
            self.imgpath = join(MYDIR, '../images')
            self.game_controller = Mock()
            self.game_controller.jury_states = list(range(1, 10, 1))
            self.game_controller.get_players = Mock(return_value=[])
            self.vis_object = vis_module.FrameVisualizer(self.game_controller)

        def test__draw_frame(self):
            for i in range(9):
                self.vis_object._draw_frame(i)
                self.assertIsNotNone(self.vis_object.frame_label['image'])
                self.assertEqual(self.vis_object.frame_number, i)


    if __name__ == '__main__':
        ut.main()
