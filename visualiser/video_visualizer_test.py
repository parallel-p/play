import unittest
from unittest.mock import Mock
import visualizer
import os
import subprocess
import pickle
import shutil


class VideoVisualizerTest(unittest.TestCase):
    def setUp(self):
        painter_obj = Mock()

        def side_effect(arg1, arg2):
            open(arg1, 'x').close()
        # That will be done instead of drawing a game state.
        content = Mock()
        content.save.side_effect = side_effect
        content.size.return_value = (600, 600)
        painter_obj.paint.return_value = Mock()
        painter_obj.paint.return_value.content = content
        # We don't want to have a real video file created:
        subprocess.Popen = Mock(side_effect=lambda x: open('result.avi', 'x')
                                .close())

        if not os.path.exists('test'):
            os.mkdir('test')
        os.chdir('test')

        for i in range(100):
            with open('state{num:02d}.jstate'.format(num=i), 'wb') as file:
                pickle.dump([False, True], file)

        os.chdir('..')
        self.viz = visualizer.Visualizer(painter_obj, 'test')

    def test_get_jury_states(self):
        retv = self.viz.get_jury_states()
        self.assertEqual(len(retv), 200)

    def test_generate_images(self):
        self.viz.generate_images()
        for i in range(200):
            self.assertTrue(os.path.exists(
                            os.path.join('test', 'tempimage{num:03d}.png'
                            .format(num=i))))

    def test_collect_images2video(self):
        for i in range(200):
            open(os.path.join('test', 'tempimage{num:03d}.png'.format(num=i)),
                 'x').close()
            self.viz.file_list.append(os.path.join('test',
                                      'tempimage{num:03d}.png'.format(num=i)))
        self.viz.imagefile_name = 'tempimage%03d.png'
        self.viz.collect_images2video()
        self.assertTrue(os.path.exists('result.avi'))
        for i in range(200):
            self.assertFalse(os.path.exists(
                             os.path.join('test', 'tempimage{num:03d}.png'
                             .format(num=i))))

    def tearDown(self):
        shutil.rmtree('test')

        if (os.path.exists('result.avi')):
            os.remove('result.avi')

if __name__ == '__main__':
    unittest.main()
