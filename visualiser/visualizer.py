import subprocess
import os
import re
import pickle
from math import log10
# from PIL import Image, ImageDraw


class NoJuryStatesException(Exception):
    '''Thrown if no jury states found.'''
    pass


class Visualizer:
    '''Composes video file from game data.'''

    def __init__(self, _painter_obj, _working_dir='.',
                 _file_mask='.*\.jstate'):
        '''Constructor. Parameters:
         - _painter_obj - painter object
         - _working_dir - directory with jury states
         - _file_mask - file mask of jury state files
        '''
        self.painter = _painter_obj
        self.working_dir = _working_dir
        self.file_mask = _file_mask
        self.file_list = []
        self.imagefile_name = None
        self.video_width, self.video_height = None, None

    def get_jury_states(self):
        '''Returns a list of all jury states from the specified directory.'''
        path = list(os.walk(self.working_dir))

        if not path:
            return []

        result = []
        # We need the list of files in current directory
        # path[0] -- current directory
        # path[0][2] -- file list
        # Check help(os.wals) for details
        for fname in path[0][2]:
            if re.search(self.file_mask, fname):
                with open(os.path.join(self.working_dir, fname), 'rb') as file:
                    result += pickle.load(file)
        return result

    def collect_images2video(self):
        '''Composes a video file from painted images.'''
        if not self.imagefile_name:
            raise Exception("Frames have not been generated: please call"
                            " generate_images() first.")

        subprocess.Popen(('ffmpeg -f -i ' + os.path.join(self.working_dir,
                         self.imagefile_name) + ' -r 2 -s ' +
                         str(self.video_width) + 'x' + str(self.video_height)
                         + ' result.avi').split())
        # Removing generated images:
        for filename in self.file_list:
            os.remove(filename)

    def generate_images(self):
        '''Generates frames for video.'''
        jstates = self.get_jury_states()

        if not jstates:
            raise NoJuryStatesException('Folder ' + self.working_dir +
                                        ' is empty. No images to collect.')

        # We need filenames with leading zeroes for ffmpeg
        zero_count = int(log10(len(jstates)) + 1)
        self.imagefile_name = 'tempimage%0{}d.png'.format(zero_count)

        for ind, jstate in enumerate(jstates):
            image = self.painter.paint(jstate).content
            self.file_list.append(os.path.join(self.working_dir, ('tempimage{}'
                                  '.png').format(str(ind).zfill(zero_count))))
            image.save(self.file_list[-1], 'png')
            self.video_width, self.video_height = image.size()
