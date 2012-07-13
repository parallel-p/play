import subprocess
import os
import pickle
import re
import getimageinfo
from math import log10


class NoJuryStatesException(Exception):
    '''Thrown if no jury states found.'''
    pass

TEMPFILE_NAME = 'tempvideo.mpg'


class VideoVisualizer:
    '''Composes video file from game data.'''

    def __init__(self, _framerate, _painter_obj, _file_mask, _working_dir='.'):
        '''Constructor. Parameters:
         - _painter_obj - painter object
        '''
        self.painter = _painter_obj()
        self.file_mask = _file_mask
        self.working_dir = _working_dir
        self.framerate = _framerate
        self.file_list = None
        self.imagefile_name = None
        self.counter = 0

    def _get_game_controller(self, filename):
        '''Unpickles a game controller.'''
        try:
            with open(filename, "rb") as file:
                return pickle.load(file)
        except:
            raise NoJuryStatesException('GameController in file ' + filename +
                                        ' contains no jury states.')

    def _generate_game_images(self, jstates):
        '''Generates frames for video.'''

        # We need filenames with leading zeroes for ffmpeg
        zero_count = int(log10(len(jstates)) + 1)
        self.file_list = []
        ext = None
        for ind, jstate in enumerate(jstates):
            image = self.painter.paint(jstate)
            # Get size from tuple (type, width, height)
            self.size = [0, 0]
            ext, self.size[0], self.size[1] = getimageinfo.getImageInfo(image)
            self.file_list.append(os.path.join(self.working_dir, ('tempimage' +
                                  str(ind).zfill(zero_count) + '.' + ext)))
            with open(self.file_list[-1], "wb") as f:
                f.write(image)

        self.imagefile_name = ('tempimage%0{}d.' + ext).format(zero_count)

    def _collect_game_images_to_video(self, jstates):
        '''Composes a video file from all images in folder images.'''

        self._generate_game_images(jstates)

        subprocess.call(('ffmpeg -f -i {} -r {} -s {}x{} {}'.
                        format(os.path.join(self.working_dir, self.imagefile_name),
                        self.framerate,
                        self.size[0],
                        self.size[1],
                        TEMPFILE_NAME).split()))

        # Removing generated images:
        for filename in self.file_list:
            os.remove(filename)

    def generate_tournament_status(self, game_controller):
        pass

    def compile(self, output_name):
        controllers = []
        for filename in os.listdir(self.working_dir):
            if re.search(self.file_mask, filename):
                controllers.append(self._get_game_controller(os.path.join(
                                   self.working_dir, self.filename)))

        controllers = list(sorted(controllers))

        name, extension = output_name.split(sep='.')

        with open(name + ".mpg", "wb") as result:
            for controller in controllers:
                self._generate_tournament_status(controller)
                self._collect_game_images_to_video(controller.jury_states)
                with open(TEMPFILE_NAME, 'rb') as file:
                        result.write(file.read())
                os.remove(TEMPFILE_NAME)

        subprocess.call(('ffmpeg -i ' + name + '.mpg -sameq ' + output_name)
                        .split())
