import subprocess
import os
import pickle
import re
import shutil
import tempfile
from game_controller import GameController
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


class VideoVisualizer:
    '''Composes video file from game data.'''

    def __init__(self, _framerate, _painter_obj, _file_mask, _working_dir='.',
                 _silent=False, _table_drawer=None):
        '''
        Constructor. Parameters:
            * _framerate - framerate of video (max=24)
            * _painter_obj - painter class
            * _file_mask - file mask of GameController files (regular
            expression)
            * _working_dir - directory with GameController files
            * _silent - if True, compiler will write nothing to screen
        '''
        self.painter = _painter_obj
        self.table_drawer = _table_drawer
        self.file_mask = _file_mask
        self.working_dir = _working_dir
        self.framerate = _framerate
        self.inframe = int(48.0 / _framerate)
        self.file_list = None
        # Image filemask given to ffmpeg
        self.imagefile_name = None
        # Image size
        self.size = None
        self._paths = [os.path.abspath('.'), tempfile.mkdtemp()]
        self._frame_count = 0
        self.log = not _silent
        self._tempfiles = []
        self.ext = None
        self.mode = None

    def _create_tempfile(self, suffix=''):
        self._tempfiles.append(tempfile.mkstemp(suffix))
        return self._tempfiles[-1]

    def _change_path(self, num):
        if num == 1 and os.path.abspath('.') != self._paths[1]:
            self._paths[0] = os.path.abspath('.')
        os.chdir(self._paths[num])

    def _create_frame(self, fname, number):
        self._change_path(1)
        begname = '{:09d}'.format(self._frame_count) + self.ext
        shutil.copyfile(fname[1], begname)
        for loop in range(number * self.inframe - 1):
            os.link(begname, '{:09d}'.format(self._frame_count +\
                                             loop + 1) + self.ext)
        self._frame_count += self.inframe * number
        self._change_path(0)
        os.close(fname[0])
        os.remove(fname[1])

    def _get_game_controller(self, filename):
        '''Unpickles a game controller.'''
        with open(filename, 'rb') as file:
            return pickle.load(file)

    def _generate_game_images(self, controller):
        '''Generates frames for video.'''
        if len(controller.jury_states) == 0:
            if self.ext is None:
                raise NoJuryStatesException('First GameController contains no '
                                            'jury states - cannot visualize '
                                            'an empty game.')
            else:
                print('One of GameControllers consists no jury states - the '
                      'game will be empty.')
        # We need filenames with leading zeroes for ffmpeg
        zero_count = int(log10(len(controller.jury_states)) + 1)
        file_list = []
        painter = self.painter(controller._players)
        for ind, jstate in enumerate(controller.jury_states):
            if self.log:
                print(chr(13) + '    Generating game images... {}/{}'\
                    .format(ind + 1, len(controller.jury_states)), end='')
            image = painter.paint(jstate)
            self.ext = self.ext or get_image_format(image)
            file_list.append(self._create_tempfile(self.ext))
            with open(file_list[-1][1], 'wb') as f:
                f.write(image)
            if self.size is None or self.mode is None:
                im = Image.open(file_list[-1][1])
                self.size = im.size
                self.mode = im.mode
        return file_list

    def _draw_tournament_status(self, round_id):
        if self.table_drawer is not None:
            tfile = self._create_tempfile(self.ext)
            with open(tfile[1], 'wb') as f:
                imagew = self.table_drawer(os.path.join(self.working_dir,
                         'tournament.data'), round_id, self.mode, self.ext)
                f.write(imagew)
            im = Image.open(tfile[1])
            ratio = min(self.size[0] / im.size[0], self.size[1] / im.size[1])
            ratio_turned = min(self.size[1] / im.size[0],
                               self.size[0] / im.size[1])
            if ratio_turned > ratio:
                im = im.transpose(Image.ROTATE_270)
                im = im.resize((int(im.size[0] * ratio_turned), int(im.size[1] * ratio_turned)), Image.ANTIALIAS)
            else:
                im = im.resize((int(im.size[0] * ratio),
                                int(im.size[1] * ratio)), Image.ANTIALIAS)
            res = Image.new(self.mode, self.size, 'white')
            res.paste(im, ((self.size[0] - im.size[0]) // 2,
                           (self.size[1] - im.size[1]) // 2,
                           (self.size[0] + im.size[0]) // 2,
                           (self.size[1] + im.size[1]) // 2))
            resfile = self._create_tempfile(self.ext)
            res.save(resfile[1], self.ext[1:])
            del im
            os.close(tfile[0])
            os.remove(tfile[1])
            self._create_frame(resfile, 2 * self.framerate)

    def generate_tournament_status(self, contr):
        '''Generates a frame with a tournament status.'''
        temptitle = self._create_tempfile(self.ext)
        # Text displayed on the frame:
        info = (wrap('Tournament: ' + str(contr.signature.tournament_id),
                     width=40) +
                wrap('Round:      ' + str(contr.signature.round_id) + (
                    '' if contr.signature.round_name is None else (
                        '(' + contr.signature.round_name + ')')), width=40) +
                wrap('Series:     ' + str(contr.signature.series_id),
                     width=40) +
                wrap('Game:       ' + str(contr.signature.game_id), width=40) +
                [''] +
                wrap('Players: ' + ', '.join(map(lambda x: x.bot_name + ' by ' + x.author_name,
                     contr._players)), width=40))

        im = Image.new(self.mode, self.size, 'blue')
        draw = ImageDraw.Draw(im)
        cfsize = 100
        done_once = False
        # Here we should find the best fitting font size.
        self._change_path(0)
        while True:
            font = ImageFont.truetype(os.path.join('fonts',
                                      'Lucida Console.ttf'), cfsize,
                                      encoding='unic')
            textlen = max(map(lambda x: font.getsize(x)[0], info))
            textheight = (font.getsize('T')[1] + 1) * len(info)
            if (textlen < self.size[0] - 10 and textheight < self.size[1] - 10
                    and done_once):
                break
            done_once = True
            cfsize = min(cfsize - 1, int(cfsize * min((self.size[0] - 10)
                         / textlen, (self.size[1] - 10) / textheight)))
        # Distance between corners of texts, starting position:
        dy = font.getsize('T')[1] + 1
        y = (self.size[1] - dy * len(info)) / 2
        # Finally, we draw it:
        for line in info:
            width = font.getsize(line)[0]
            draw.text(((self.size[0] - width) / 2, y), line, font=font,
                      fill=(255, 255, 255))
            y += dy
        im.save(temptitle[1])
        # Compiling a video file:
        self._create_frame(temptitle, 2 * self.framerate)

    def compile(self, output_name):
        '''
        Compiles all games given by the specified filemask into one video file.
        The file will be saved into the log folder.
        '''
        controllers = []
        for filename in os.listdir(self.working_dir):
            if re.search(self.file_mask, filename):
                controllers.append(self._get_game_controller(os.path.join(
                                   self.working_dir, filename)))
        # The games should be given in the right order:
        controllers = list(sorted(controllers))

        vfile_list = []
        prev_rnd = controllers[0].signature.round_id
        for ind, controller in enumerate(controllers):
            if self.log:
                print('Processing game {}:{}:{}:{} ({} of {}):'.format(
                      controller.signature.tournament_id,
                      controller.signature.round_id,
                      controller.signature.series_id,
                      controller.signature.game_id, ind + 1, len(controllers)))
            t = self._generate_game_images(controller)
            if controller.signature.round_id > prev_rnd:
                prev_rnd = controller.signature.round_id
                self._draw_tournament_status(prev_rnd)
            self.generate_tournament_status(controller)
            if self.log:
                print('\n    Creating frames...')
            for fname in t:
                self._create_frame(fname, 1)

        self._draw_tournament_status(prev_rnd + 1)
        self._change_path(1)
        print('Compiling the video file...')
        try:
            with open(os.devnull, 'w') as fnull:
                subprocess.Popen('ffmpeg -i %09d{} -r 48 -s {}x{} {}'.format(
                                 self.ext, self.size[0], self.size[1],
                                 output_name).split(), stderr=fnull,
                                 stdin=subprocess.PIPE).communicate(
                                 'y\n'.encode() * 10)
            self._change_path(0)
            shutil.copyfile(os.path.join(self._paths[1], output_name),
                            os.path.join(self.working_dir, output_name))
        except FileNotFoundError:
            raise FileNotFoundError('You need to install ffmpeg to create'
                                    ' videos.')
        print('Compiling finished.')

    def __del__(self):
        if self.log:
            print('Cleaning up...')
        for fname in self._tempfiles:
            if os.path.exists(fname[1]):
                os.close(fname[0])
                os.remove(fname[1])
        shutil.rmtree(self._paths[1])
