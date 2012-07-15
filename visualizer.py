import subprocess
import os
import pickle
import re
import shutil
from textwrap import wrap
from PIL import Image, ImageDraw, ImageFont
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
TEMPFILE_NAME_TITLE = 'temptitle.mpg'


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
        try:
            subprocess.call(('ffmpeg -f image2 -i {} -r 48 -s {}x{} {}'.
                            format(os.path.join(self.working_dir,
                            self.imagefile_name), self.size[0], self.size[1],
                            TEMPFILE_NAME).split()))
        except FileNotFoundError:
            raise FileNotFoundError('You need to install ffmpeg to make video'
                                    ' files.')
        finally:
            # Removing generated images:
            for filename in self.file_list:
                os.remove(filename)


    def generate_tournament_status(self, contr):
        '''Generates a frame with a tournament status.'''
        TEMPIMAGEFILE_TITLE = 'tempimage_title{:03d}.png'
        TEMP_FOR_FFMPEG = 'tempimage_title%03d.png'
        # Text displayed on the frame:
        info = (wrap('Tournament: ' + str(contr.signature.tournament_id),
                     width=40) +
                wrap('Round:      ' + str(contr.signature.round_id),
                     width=40) +
                wrap('Series:     ' + str(contr.signature.series_id),
                     width=40) +
                wrap('Game:       ' + str(contr.signature.game_id), width=40) +
                [''] +
                wrap('Players: ' + ', '.join(map(lambda x: x.author_name,
                     contr.players)), width=40))

        im = Image.new('RGB', self.size, (0, 0, 255))
        draw = ImageDraw.Draw(im)
        cfsize = 100
        done_once = False
        # Here we should find the best fitting font size.
        while True:
            font = ImageFont.truetype('Lucida Console.ttf', cfsize,
                                      encoding='unic')
            textlen = max(map(lambda x: font.getsize(x)[0], info))
            textheight = (font.getsize('T')[1] + 1) * len(info)
            if (textlen < self.size[0] - 10 and textheight < self.size[1] - 10
                    and done_once):
                break
            done_once = True
            cfsize = min(cfsize - 1, int(cfsize * min((self.size[0] - 10)
                         / textlen, (self.size[1] - 10) / textheight)))
        # Distance between corners of texts:
        dy = font.getsize('T')[1] + 1
        # Starting position:
        y = (self.size[1] - dy * len(info)) / 2
        # Finally, we draw it:
        for line in info:
            width = font.getsize(line)[0]
            draw.text(((self.size[0] - width) / 2, y), line, font=font,
                      fill=(255, 255, 255))
            y += dy
        im.save(TEMPIMAGEFILE_TITLE.format(0))

        TIME_IN_SEC = 5
        # We have to clone the frame (see the explanation above):
        for i in range(24 * TIME_IN_SEC - 1):
            shutil.copyfile(TEMPIMAGEFILE_TITLE.format(0),
                            TEMPIMAGEFILE_TITLE.format(i + 1))
        # Compilind into a video file:
        try:
            subprocess.call(('ffmpeg -f image2 -i ' + TEMP_FOR_FFMPEG + ' -r 48 -s'
                            ' {}x{} {}').format(self.size[0], self.size[1],
                            TEMPFILE_NAME_TITLE).split())
        except FileNotFoundError:
            raise FileNotFoundError('You need to install ffmpeg to make video'
                                    ' files.')
        finally:
            # Cleaning up:
            for i in range(24 * TIME_IN_SEC):
                os.remove(TEMPIMAGEFILE_TITLE.format(i))

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
        name = output_name[:output_name.rfind('.')] + '1'

        with open(name + ".mpg", "wb") as result:
            for controller in controllers:
                self.collect_game_images_to_video(controller.jury_states)
                self.generate_tournament_status(controller)
                with open(TEMPFILE_NAME_TITLE, 'rb') as file:
                    result.write(file.read())
                os.remove(TEMPFILE_NAME_TITLE)
                with open(TEMPFILE_NAME, 'rb') as file:
                    result.write(file.read())
                os.remove(TEMPFILE_NAME)

        try:
            subprocess.call(('ffmpeg -i ' + name + '.mpg -sameq ' + output_name)
                            .split())
        except FileNotFoundError:
            raise FileNotFoundError('You need to install ffmpeg to make video'
                                    ' files.')
        finally:
            os.remove(name + '.mpg')
