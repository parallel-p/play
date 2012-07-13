import subprocess
import os
import pickle
import imghdr
import config
import re
import getimageinfo
from math import log10
# from PIL import Image, ImageDraw


class NoJuryStatesException(Exception):
    '''Thrown if no jury states found.'''
    pass


class VideoVisualizer:
    '''Composes video file from game data.'''

    def __init__(self, _file_mask, _working_dir='.'):
        '''Constructor. Parameters:
         - _painter_obj - painter object

        '''
        self.painter = config.Config.painter()
        self.file_mask = _file_mask
        self.working_dir = _working_dir
        self.framerate = config.Config.framerate
        self.file_list = None
        self.imagefile_name = None
        self.counter = 0

    def _get_game_controller(self, filename):
        with open(filename, "rb") as f:
            return pickle.load(f)

    def _generate_game_images(self, jstates):
        '''Generates frames for video.'''
        if not jstates:
            raise NoJuryStatesException('GameController in file ' + filename +
                                        ' contains no jury states.')

        # We need filenames with leading zeroes for ffmpeg
        zero_count = int(log10(len(jstates)) + 1)
        self.file_list = []
        ext = None
        for ind, jstate in enumerate(jstates):
            image = self.painter.paint(jstate)
            self.size = getimageinfo.getImageInfo(image)[1:]
            ext = imghdr.what('', image)
            self.file_list.append(os.path.join(self.working_dir, ('tempimage' +
                                  str(ind).zfill(zero_count) + '.' + ext)))
            with open(self.file_list[-1], "wb") as f:
                f.write(image)

        self.imagefile_name = ('tempimage%0{}d.' + ext).format(zero_count)

    def _collect_game_images_to_video(self, jstates):
        '''Composes a video file from painted images.'''
        game_controller = self._get_game_controller(filename)
        self._generate_game_images(game_controller.jury_states)

        subprocess.call(('ffmpeg -f -i ' + os.path.join(self.working_dir,
                        self.imagefile_name) + ' -r ' + str(self.framerate) +
                        ' -s ' + str(self.size[0]) + 'x' + str(self.size[1])
                        + ' tempvideo{}.mpg'.format(self.counter)).split())
        self.counter += 1
        # Removing generated images:
        for filename in self.file_list:
            os.remove(filename)

    def _generate_tournament_status(self, game_controller):
        pass

    def compile(self, res_name):
        contr_list = []
        for filename in os.listdir(self.working_dir):
            if re.search(self.file_mask, filename):
                contr_list.append(self._get_game_controller(os.path.join(
                                  self.working_dir, self.filename)))
        contr_list = tuple(sorted(contr_list))
        for cgame in contr_list:
            self._generate_tournament_status(cgame)
            self._collect_game_images_to_video(cgame.jstates)
        old_ext = res_name[res_name.rfind('.'):]
        res_name = res_name[:res_name.rfind('.')]
        with open(res_name + ".mpg", "wb") as result:
            for loop in range(self.counter):
                with open('tempvideo' + str(loop) + '.mpg', 'rb') as tempfile:
                    result.write(tempfile.read())
                os.remove('tempvideo' + str(loop) + '.mpg')
        subprocess.call(('ffmpeg -i ' + res_name + '.mpg -sameq ' + res_name +
                        old_ext).split())
