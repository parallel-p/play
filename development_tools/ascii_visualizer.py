# -*- coding: utf-8 -*-
# This class is responsible for visualizing a game in ascii art,
# if the game's painter supports this feature

DEBUG = False

import colorama
from colorama import Fore, Back, Style
import colorama.ansitowin32 as ansi2w32
import config
from lib.keyboard_capture import getch
from time import sleep
from os import name, system


def _clear():
    '''this function clears the console by executing the appropriate command'''
    if name == 'posix':
        system('clear')
    elif name == 'nt':
        system('cls')
    else:
        raise Exception('I can\'t recognise your OS')


class AsciiVisualizer:
    ''' This class represents an ASCII visualizer - a console
    utility, which represents a game in ASCII-art graphics, if
    the painter supports this feature. '''

    def __init__(self, game_controller):
        ''' ``game_controller`` - an object, which has a ``jury_states``
        field, that is an enumeration of ``JuryState`` objects, which
        will be passed to the painter. '''
        self.output_string = ''
        self.painter_factory = config.Painter
        self.game_controller = game_controller
        self.frame_number = 0
        if name == 'nt':
            self.key_sets = {
                'next':'DdNn.>]}+= ',
                'prev':'BbAa|,<[{-_',
                'jump':'0123456789SsJjFfRrGg',
                'auto':'WwMmPp',
                'quit':'QqXx'
                }
        else:
            self.key_sets = {
                'next':'Nn.>]}+= \r\n',
                'prev':'Bb\|,<[{-_',
                'jump':'0123456789JjFfRrGg',
                'auto':'AaMmPp',
                'quit':'QqEe'
                }

    def _frame2string(self, new_frame_number):
        self.frame_number = new_frame_number
        return '{color}Frame #{0:04d} of {1:d} :{nocolor}\n{2:s}\n'.format(
            self.frame_number + 1, self._jury_state_count(),
            self.painter_factory(self.game_controller.get_players())\
                .ascii_paint(
                    self.game_controller.jury_states[new_frame_number]),
            color=Fore.YELLOW + Style.BRIGHT,
            nocolor=Fore.RESET + Style.NORMAL)

    def _jury_state_count(self):
        return len(self.game_controller.jury_states)

    def _help(self):
        '''prints a help screen for the visualizer'''
        if name == 'nt':
            msg = '''{brt}{bl}Navigation help:
                ____
               |{gr} W  {bl}|
               |{mg}auto{bl}|
          ____  ____  ____
         |{gr} A  {bl}||{gr} S  {bl}||{gr} D  {bl}|
         |{mg}prev{bl}||{mg}jump{bl}||{mg}next{bl}|

        forward       : {gr}D,N,SPACE{bl}             (Alt: {gr}>,],+{bl})
        back          : {gr}A,B{bl}              (Alt: {gr}<,[,-{bl})
        jump to frame : {gr}S,J,G,all numerals{bl} (Alt: {gr}F,R{bl}  )

        autoplay      : {gr}W,M,P{bl}
        stop autoplay : {gr}Ctrl-Z{bl}

        quit          : {gr}Q,''X{bl}

        display this message : {gr}any other key{norm}
        '''
        else:
            msg = '''{brt}{bl}Navigation help:
                ____
               |{gr} Up {bl}|
               |{mg}auto{bl}|
          ____  ____  ____
         |{gr}Left{bl}||{gr}Down{bl}||{gr}Righ{bl}|{gr}t{bl}
         |{mg}prev{bl}||{mg}jump{bl}||{mg}next{bl}|

        forward       : {gr}RIGHT,N,SPACE,ENTER{bl}   (Alt: {gr}>,],+{bl})
        back          : {gr}LEFT,B,\{bl}                (Alt: {gr}<,[,-{bl})
        jump to frame : {gr}DOWN,J,G,all numerals{bl} (Alt: {gr}F,R{bl}  )

        autoplay      : {gr}UP,A,M,P{bl}
        stop autoplay : {gr}^C{bl}

        quit          : {gr}Q,E{bl}

        display this message : {gr}any other key{norm}
        '''
        print(msg.format(
            gr=Fore.GREEN, bl=Fore.BLUE, mg=Fore.MAGENTA,
            brt=Style.BRIGHT, norm=Style.NORMAL) + Fore.RESET)

    def _error(self, msg):
        '''prints an error message in bright red color'''
        print(Fore.RED + Style.BRIGHT + msg + Style.NORMAL + Fore.RESET)

    def _prompt(self, msg):
        '''prints a prompt in bright yellow color'''
        print(Fore.YELLOW + Style.BRIGHT + msg, end=' : '
        + Style.NORMAL + Fore.RESET)

    def activate(self):
        ''' Like ``FrameVisualizer``, ``AsciiVisualizer`` won't start
        on init - if you want to see the output, you have to invoke this
        method. '''
        colorama.init()
        _clear()
        key='any'
        self._help()
        print(Fore.MAGENTA + Style.BRIGHT + 'Press Any Key to begin...')
        getch()
        _clear()
        print(self._frame2string(0))
        self.nextc=False
        self.prevspec=False
        while True:
            if DEBUG:
                print(repr(key))
            key = getch()
            arrow=None
            if self.nextc:
                if key in 'ABCD':
                    arrow=key
                else:
                    arrow=None
                self.nextc=False
            elif self.prevspec and key == '[':
                self.nextc=True
                self.prevspec=False
                continue
            elif name=='posix' and key == '\x1b':
                self.prevspec=True
                continue
            if DEBUG:
                if arrow is not None:
                    print('Arrow ', end = arrow)
                
                if key in self.key_sets['auto']:
                    print ('AAAAAAAAAAAAA!!!!')
                elif key in self.key_sets['jump']:
                    print ('Beam me up, Scotty!')
                elif key in self.key_sets['next']:
                    print ('Run, forest, run!')
                elif key in self.key_sets['prev']:
                    print('Everybody fall back!')
                if key == 'q':
                    break
                continue
            if name == 'nt':
                try:
                    key=key.decode()
                except UnicodeDecodeError:
                    self._error('I cannot recognise the key you just pressed')
                    continue
            if arrow == 'C' or key in self.key_sets['next']:#next
                _clear()
                if self.frame_number < self._jury_state_count() - 1:
                    print(self._frame2string(self.frame_number + 1))
                else:
                    print(self._frame2string(self.frame_number))
                    self._error('this is the last frame.')
            elif arrow == 'D' or key in self.key_sets['prev']:#prev
                _clear()
                if self.frame_number > 0:
                    print(self._frame2string(self.frame_number - 1))
                else:
                    print(self._frame2string(self.frame_number))
                    self._error('this is the first frame.')
            elif arrow == 'A' or key in self.key_sets['auto']:
                while True:
                    self._prompt(
                        'Enter FPS and the last frame (optional)')
                    reply = input()
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
                                while (
                                    (self.frame_number + addv) < jscount) and (
                                        self.frame_number + addv) >= 0 and (
                                            self.frame_number != endframe):
                                    _clear()
                                    print(self._frame2string(
                                        self.frame_number + addv))
                                    sleep(time)
                            except KeyboardInterrupt:
                                pass
                            break
                    self._error('The speed must be a real nonzero number')
            elif key in self.key_sets['quit']:
                print('Quit')
                return None
            elif arrow == 'B' or key in self.key_sets['jump']:
                while True:
                    self._prompt('Enter frame number')
                    frame = input()
                    # Add some fool-protection...
                    if frame.isnumeric():
                        number = int(frame) - 1
                        if number >= 0 and number < self._jury_state_count():
                            _clear()
                            print(self._frame2string(number))
                            break
                        else:
                            self._error('No such frame.')
                    else:
                        self._error('enter a NUMBER.')
            else:
                _clear()
                print(self._frame2string(self.frame_number))
                self._help()
        colorama.deinit()

    def dump(self, writable):
        ''' Dumps full game into something writable. '''
        for index, jury_state in enumerate(self.game_controller.jury_states):
            writable.write('Frame #{0:d}:\n{1:s}\n'.format(
                index, self.painter_factory(
                    self.game_controller.get_players()).ascii_paint(jury_state)))
