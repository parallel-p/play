# This class is responsible for visualizing a game in ascii art,
# if painter supports such feature

import config
from lib.keyboard_capture import getch
from time import sleep

def _clear():
    '''this function clears the console by executing the appropriate command'''
    from os import name, system
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

    def _frame2string(self, new_frame_number):
        self.frame_number = new_frame_number
        return 'Frame #{0:04d} of {1:04d} :\n{2:s}\n'.format(
            self.frame_number + 1, 
            self._jury_state_count(),
            
            self.painter_factory().ascii_paint(
            self.game_controller.jury_states[new_frame_number]))

    def _jury_state_count(self):
        return len(self.game_controller.jury_states)
    
    def _help(self):
        '''prints a help screen for the visualizer'''
        print('''Navigation:
        forward       : N,ENTER,SPACE  (Alt: >,],+)
        back          : B,P,\          (Alt: <,[,-)
        jump to frame : J,G,any number (Alt: F,R  )

        autoplay      : A,M
        stop autoplay : ^C 

        quit          : Q,E
        ''')

    def activate(self):
        ''' Like ``FrameVisualizer``, ``AsciiVisualizer`` won't start
        on init - if you want to see the output, you have to invoke this
        method. '''
        print(self._frame2string(0))
        self._help()
        while True:
            key = getch()
            if (key == key in 'Nn.>]}+=\n '):
                _clear()
                if self.frame_number < self._jury_state_count() - 1:
                    print(self._frame2string(self.frame_number + 1))
                else:
                    print(self._frame2string(self.frame_number))
                    print('this is the last frame')
            elif key in 'BbPp\|,<[{-_' :
                _clear()
                if self.frame_number > 0:
                    print(self._frame2string(self.frame_number - 1))
                else: 
                    print(self._frame2string(self.frame_number))
                    print('this is the first frame.')
            elif key in 'AaMm' :
                print('Enter speed(frames/sec), and, optionally, the ending frame:', end=' ')
                cmd=input().split()
                try:
                    speed=float(cmd[0])
                except ValueError:
                    speed=0
                if speed is not 0:
                    jscount=self._jury_state_count()

                    if speed>=0:
                        addv=1
                        time=1/speed
                    else:
                        addv=-1
                        time=-1/speed
    
                    if len(cmd)>1 and cmd[1].isnumeric():
                        endframe=int(cmd[1])-1
                    else:
                        endframe=jscount
            
                    try:
                        while (self.frame_number+addv) < jscount and (self.frame_number+addv)>=0 and self.frame_number!=endframe:
                            _clear()
                            print(self._frame2string(self.frame_number + addv))
                            sleep(time)
                    except KeyboardInterrupt:
                        pass
                else:
                    print('The speed must be a real nonzero number')
                    
            elif key in 'QqEe':
                print('Quit')
                return None
            elif key in '0123456789JjFfRrGg':
                while True:
                    print('Enter frame number:', end=' ')
                    frame = input()
                    # Add some fool-protection...
                    if frame.isnumeric():
                        number = int(frame) - 1
                        if number >= 0 and number < self._jury_state_count():
                            _clear()
                            print(self._frame2string(number))
                            break
                        else:
                            print('No such frame.')
                    else:
                        print('enter a NUMBER.')
            else:
                self._help()
