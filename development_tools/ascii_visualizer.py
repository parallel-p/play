# -*- coding: utf-8 -*-
''' This class is responsible for visualizing a game in ascii art,
    if the game's painter supports this feature.
'''

DEBUG = False

import lib.colorama as colorama
from lib.colorama import Fore, Back, Style
import lib.colorama.ansitowin32 as ansi2w32
import config
from lib.keyboard_capture import getch
from time import sleep
from os import name, system
from threading import Thread, Lock
from shutil import get_terminal_size
from math import ceil

def _clear():
    '''this function clears the console by executing the appropriate command'''
    if name == 'posix':
        system('clear')
    elif name == 'nt':
        system('cls')
    else:
        raise Exception('I can\'t recognise your OS')


def clear_string(y=None):
    pos = lambda y, x: '\x1b[{};{}H'.format(y, x)
    if y:
        x = 0 if name == 'posix' else 1
        msg = pos(y, x)
    else:
        msg = chr(13)
    print(msg + ' ' * 99 + chr(13), end='', sep='')


class AsciiVisualizer:
    ''' This class represents an ASCII visualizer - a console
    utility, which represents a game in ASCII-art graphics, if
    the painter supports this feature. '''

    def __init__(self, game_controller):
        ''' ``game_controller`` - an object, which has a ``jury_states``
        field, that is an enumeration of ``JuryState`` objects, which
        will be passed to the painter. '''
        self.output_string = ''
        self.painter_factory = config.AsciiPainter
        self.game_controller = game_controller
        self.frame_number = 0
        self.stop = False
        self.lock = Lock()
        self.prev_frame = None
        self.key_sets = {
            'next': 'Nn.>]}+= \r\n',
            'prev': 'Bb\|,<[{-_',
            'jump': '0123456789JjFfRrGg',
            'auto': 'AaMmPp',
            'quit': 'QqEe'
            }

    def _jury_state_count(self):
        return len(self.game_controller.jury_states)

    def _help(self):
        '''prints a help screen for the visualizer'''
        pos = lambda y, x: '\x1b[{};{}H'.format(y, x)
        msg = '''{brt}{bl}Navigation help:
          ____     ____  ____  ____
         |{gr}HOME{bl}|   |{gr}PgUp{bl}||{gr} Up {bl}||{gr}PgDn{bl}|
         |{mg}1st {bl}|   |{mg}RW5%{bl}||{mg}auto{bl}||{mg}FF5%{bl}|
          ____     ____  ____  ____
         |{gr}END {bl}|   |{gr}Left{bl}||{gr}Down{bl}||{gr}Rght{bl}|
         |{mg}last{bl}|   |{mg}prev{bl}||{mg}jump{bl}||{mg}next{bl}|

        forward         : {gr}RIGHT,N,SPACE,ENTER{bl}   (Alt: {gr}>,],+{bl})
        back            : {gr}LEFT,B,\{bl}              (Alt: {gr}<,[,-{bl})
        jump to frame   : {gr}DOWN,J,G,all numerals{bl} (Alt: {gr}F,R{bl}  )
        autoplay        : {gr}UP,A,M,P{bl}
        stop            : {gr}^C{bl}

        quit            : {gr}Q,E{bl}

        display this message : {gr}any other key{norm}
        '''
        _clear()
        x = 0 if name == 'posix' else 1
        y = 0 if name == 'posix' else 1
        print(pos(y, x), msg.format(
            gr=Fore.GREEN, bl=Fore.BLUE, mg=Fore.MAGENTA,
            brt=Style.BRIGHT, norm=Style.NORMAL) + Fore.RESET)

    def _error(self, msg, end='\n'):
        '''prints an error message in bright red color'''
        print(Fore.RED + Style.BRIGHT + msg + Style.NORMAL + Fore.RESET, end=end)

    def _prompt(self, msg):
        '''prints a prompt in bright yellow color'''
        self.lock.acquire()
        clear_string()
        print(Fore.YELLOW + Style.BRIGHT + msg, end=' : '
              + Style.NORMAL + Fore.RESET)
        reply = input()
        clear_string()
        self.lock.release()
        self._print_frame(self.frame_number)
        return reply

    def _detect_arrow(self, key):
        arrow = None
        if name == 'posix' and key == '\x1b':
            if getch() in '[O':
                key = getch()
                nixdict = {
                    'A': 'A',
                    'B': 'B',
                    'C': 'C',
                    'D': 'D',
                    'H': 'H',
                    'F': 'E'
                    }
                arrow = nixdict.get(key)
                if not arrow and key in '56':
                    k = getch() 
                    if k == '~':
                        arrow = {'5': 'U', '6': 'N'}.get(key)
        elif name == 'nt' and key == b'\xe0':
            windict = {
                b'H': 'A',
                b'P': 'B',
                b'M': 'C',
                b'K': 'D',
                b'G': 'H',
                b'O': 'E',
                b'I': 'U',
                b'Q': 'N'}
            key = getch()
            arrow = windict.get(key)

        return arrow

    def _print_frame(self, index):
        self.frame_number = index
        frame_text = '{color}Frame #{0:04d} of {1:d} :{nocolor}\n{2:s}\n'.format(
            self.frame_number + 1, self._jury_state_count(),
            self.painter_factory(self.game_controller.get_players())
                .ascii_paint(
                    self.game_controller.jury_states[index]),
            color=Fore.YELLOW + Style.BRIGHT,
            nocolor=Fore.RESET + Style.NORMAL)
        self.lock.acquire()
        _clear()
        height = get_terminal_size()[1] - 3
        frame_text = frame_text.split('\n')
        lines = len(frame_text)
        frame_text = '\n\r'.join(frame_text[:height])
        print(frame_text)
        self.lock.release()
        self.prev_frame = frame_text.split('\n')
        if lines > get_terminal_size()[1]:
            #print('')
            clear_string(height + 1)
            clear_string(height + 3)
            self._error('Increase the height of the terminal and necessarily \
press Home to see the full information', end='')
            clear_string(height + 2)

    def _print_frame_diff(self, index):
        '''
        Paints new frame using old and repaints only elements that changed
        '''
        if not self.prev_frame:
            self._print_frame(index)
            return
        self.frame_number = index
        frame_text = '{color}Frame #{0:04d} of {1:d} :{nocolor}\n{2:s}\n'.format(
            self.frame_number + 1, self._jury_state_count(),
            self.painter_factory(self.game_controller.get_players())\
                .ascii_paint(
                    self.game_controller.jury_states[index]),
            color=Fore.YELLOW + Style.BRIGHT,
            nocolor=Fore.RESET + Style.NORMAL)
        # Here we find diff between two frames
        term_height = get_terminal_size()[1] - 3
        frame_text = frame_text.split('\n')
        lines = len(frame_text)
        frame_text = frame_text[:term_height]
        pos = lambda y, x: '\x1b[{};{}H'.format(y, x)
        self.lock.acquire()
        height = len(frame_text)
        for line in range(len(frame_text)):
            if (line >= len(self.prev_frame) or frame_text[line] !=
                                                self.prev_frame[line]):
                if name == 'nt':
                    print(pos(line + 1, 1), frame_text[line], sep='')
                else:
                    print(pos(line + 1, 0), frame_text[line], sep='')
        if name == 'nt':
            print(pos(height + 1, 1), ' ' * 98, chr(13), sep='', end='')
        else:
            print(pos(height, 0), ' ' * 98, chr(13), sep='', end='')
        if lines > get_terminal_size()[1]:
            #print('')
            clear_string(height + 1)
            clear_string(height + 3)
            self._error('Increase the height of the terminal and necessarily \
press Home to see the full information', end='')
            clear_string(height + 2)
        self.lock.release()
        # Here we save current frame as previouss
        self.prev_frame = frame_text

    def _read_key(self):
        key = getch()
        arrow = self._detect_arrow(key)
        if arrow is not None:
            key = None
            return (key, arrow)

        if name == 'nt' and key is not None:
            try:
                key = key.decode()
            except UnicodeDecodeError:
                key = None
                self._error('I cannot recognise the key you just pressed')
                self.prev_frame = None
        return (key, arrow)

    def auto(self, addv, time, jscount, endframe, name):
        while (self.frame_number + addv < jscount and
                self.frame_number + addv >= 0 and
                    self.frame_number != endframe):
            self._print_frame_diff(self.frame_number + addv)
            sleep(time)
            if self.stop:
                self.stop = False
                break

    def activate(self):
        thread = None
        ''' Like ``FrameVisualizer``, ``AsciiVisualizer`` won't start
        on init - if you want to see the output, you have to invoke this
        method. '''
        colorama.init()
        _clear()
        self._help()
        self.prev_frame = None
        print(Fore.MAGENTA + Style.BRIGHT + 'Press Any Key to begin...')
        self._detect_arrow(getch())
        self._print_frame_diff(0)
        self.nextc = False
        self.prevspec = False
        try:
            while True:
                (key, arrow) = self._read_key()
                self.stop = True
                if arrow is None and key is None:
                    continue
                if arrow == 'H':
                    self._print_frame_diff(0)
                elif arrow == 'E':
                    self._print_frame_diff(len(self.game_controller.jury_states) - 1)
                elif arrow == 'N':
                    self._print_frame_diff(
                        min(
                            len(self.game_controller.jury_states) - 1,
                            self.frame_number +
                                ceil(len(self.game_controller.jury_states) / 20)
                        )
                    )
                elif arrow == 'U':
                    self._print_frame_diff(
                        max(0, self.frame_number -
                            ceil(len(self.game_controller.jury_states) / 20))
                    )
                elif arrow == 'C' or arrow is None and key in self.key_sets['next']:  # next
                    if self.frame_number < self._jury_state_count() - 1:
                        if name == 'posix':
                            self._print_frame_diff(self.frame_number + 1)
                        else:
                            self._print_frame_diff(self.frame_number + 1)
                    else:
                        self._print_frame_diff(self.frame_number)
                        self._error('this is the last frame.')
                elif arrow == 'D' or arrow is None and key in self.key_sets['prev']:  # prev
                    if self.frame_number > 0:
                        self._print_frame_diff(self.frame_number - 1)
                    else:
                        self._print_frame_diff(self.frame_number)
                        self._error('this is the first frame.')
                elif arrow == 'A' or arrow is None and key in self.key_sets['auto']:
                    while True:
                        reply = self._prompt(
                            'Enter FPS and, optionally, the frame to stop on (separated by a space)')
                        if reply:
                            cmd = reply.split()
                            try:
                                speed = float(cmd[0])
                            except ValueError:
                                speed = 0
                            if speed:
                                jscount = self._jury_state_count()
                                if speed >= 0:
                                    addv = 1
                                    time = 1 / speed
                                else:
                                    addv = -1
                                    time = -1 / speed
                                if len(cmd) > 1 and cmd[1].isnumeric():
                                    endframe = int(cmd[1]) - 1
                                else:
                                    endframe = jscount
                                try:
                                    if not thread or not thread.is_alive():
                                        self.stop = False
                                        self.prev_frame = None
                                        thread = Thread(target=self.auto,
                                                        args=(addv, time, jscount, endframe, name))
                                        thread.start()
                                except KeyboardInterrupt:
                                    _clear()
                                    self._print_frame(self.frame_number)
                                break
                        self._error('The speed must be a real nonzero number')
                elif arrow is None and key in self.key_sets['quit']:
                    print('Quit')
                    return None
                elif arrow == 'B' or arrow is None and key in self.key_sets['jump']:
                    while True:
                        frame = self._prompt('Enter frame number')
                        # Add some fool-protection...
                        if frame.isnumeric():
                            number = int(frame) - 1
                            if number >= 0 and number < self._jury_state_count():
                                self._print_frame(number)
                                break
                            else:
                                if number < 0:
                                    self._error('Enter a positive integer.')
                                else:
                                    self._error('No such frame.')
                        else:
                            self._error('Enter a positive integer.')
                else:
                    self._print_frame(self.frame_number)
                    self._help()
                    self.prev_frame = None
        finally:
            _clear()
            colorama.deinit()

    def dump(self, writable):
        ''' Dumps full game into something writable. '''
        for index, jury_state in enumerate(self.game_controller.jury_states):
            writable.write('Frame #{0:d}:\n{1:s}\n'.format(
                index, self.painter_factory(
                    self.game_controller.get_players()).ascii_paint(jury_state)))
