import subprocess
import os
import pickle
import re
from PIL import Image
from math import log10


def get_image_format(data):
    '''Gets image format from its data (bytearray).'''
    # Source: getimageinfo.py (from code.google.com)
    if data[:3] == b'GIF':
        return '.gif'
    elif data.startswith(b'\211PNG\r\n\032\n'):
        return '.png'
    elif data.startswith(b'\377\330'):
        return '.jpeg'


class NoJuryStatesException(Exception):
    '''Thrown if no jury states found.'''
    pass


TEMPFILE_NAME = 'tempvideo.mpg'


class VideoVisualizer:
    '''Composes video file from game data.'''

    def __init__(self, _framerate, _painter_obj, _file_mask, _working_dir='.'):
        '''
        Constructor. Parameters:
            * _framerate - framerate of video (max=24)
            * _painter_obj - painter object
            * _file_mask - file mask of GameController files (regular
            expression)
            * _working_dir - directory with GameController files
        '''
        self.painter = _painter_obj
        self.file_mask = _file_mask
        self.working_dir = _working_dir
        self.framerate = _framerate
        self.file_list = None
        # Image filemask given to ffmpeg
        self.imagefile_name = None
        # Image size
        self.size = None

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
        repeat = max(int(48.0 / self.framerate), 1)
        # We need filenames with leading zeroes for ffmpeg      
        zero_count = int(log10(len(jstates) * repeat) + 1)
        self.file_list = []
        ext = None
        for ind, jstate in enumerate(jstates):
            image = self.painter.paint(jstate)
            ext = ext or get_image_format(image)
            # Unfortunately, MPEG1/2 format does not support any framerates
            # lower than 24 fps. So we have to clone images:
            for loop in range(repeat):
                self.file_list.append(os.path.join(self.working_dir,
                                      ('tempimage' + str(ind * repeat + loop)
                                      .zfill(zero_count) + ext)))
                with open(self.file_list[-1], "wb") as f:
                    f.write(image)
            self.size = self.size or Image.open(self.file_list[-1]).size
        self.imagefile_name = ('tempimage%0{}d' + ext).format(zero_count)

    def collect_game_images_to_video(self, jstates):
        '''Composes a video file from jury states list.'''
        self._generate_game_images(jstates)

        # The command below compiles images into a video file:  
        subprocess.call(('ffmpeg -f image2 -i {} -r 48 -s {}x{} {}'.
                        format(os.path.join(self.working_dir,
                        self.imagefile_name), self.size[0], self.size[1],
                        TEMPFILE_NAME).split()))

        # Removing generated images:
        for filename in self.file_list:
            os.remove(filename)        
                                   
    def generate_tournament_status(self, game_controller):                    
        '''Generates a frame with a tournament status (currently disabled).'''
        pass

    def compile(self, output_name):
        '''
        Compiles all games given by the specified filemask into one video file.
        '''
        controllers = []
        for filename in os.listdir(self.working_dir):
            if re.search(self.file_mask, filename):
                controllers.append(self._get_game_controller(os.path.join(
                                   self.working_dir, filename)))
        # The games should be given in the right order:         
        controllers = list(sorted(controllers))

        output_name = os.path.join(self.working_dir, output_name)
        name, extension = output_name.split(sep='.')            
        name += '1'

        with open(name + ".mpg", "wb") as result:
            for controller in controllers:
                self.generate_tournament_status(controller)
                self.collect_game_images_to_video(controller.jury_states)
                with open(TEMPFILE_NAME, 'rb') as file:
                    result.write(file.read())
                os.remove(TEMPFILE_NAME)
        subprocess.call(('ffmpeg -i ' + name + '.mpg -sameq ' + output_name)
                        .split())
        os.remove(name + '.mpg')
