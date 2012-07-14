# This class is responsible for visualizing a game in ascii art,
# if painter supports such feature

import config
from keyboard_capture import getch


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
    the painter supports such feature. '''

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
        return 'Frame #{0:d}:\n{1:s}\n'.format(
            self.frame_number + 1, self.painter_factory().ascii_paint(
                self.game_controller.jury_states[new_frame_number]))

    def _jury_state_count(self):
        return len(self.game_controller.jury_states)

    def activate(self):
        ''' Like ``FrameVisualizer``, ``AsciiVisualizer`` won't start
        on init - if you want to see the output, you have to invoke this
        method. '''
        print('''Use B and N keys for navigation. Use Q to quit.
Any other key will call prompt for a frame number.
''')
        print(self._frame2string(0))
        while True:
            key = getch()
            _clear()
            if (key == ' ' or key in 'Nn') and (
                    self.frame_number < self._jury_state_count() - 1):
                print(self._frame2string(self.frame_number + 1))
            elif key in 'Bb' and self.frame_number > 0:
                print(self._frame2string(self.frame_number - 1))
            elif key in 'Qq':
                print('Quit')
                return None
            else:
                while True:
                    print('Enter frame number:', end=' ')
                    frame = input()
                    # Add some fool-protection...
                    if frame.isnumeric():
                        number = int(frame) - 1
                        if number >= 0 and number < self._jury_state_count():
                                print(self._frame2string(number))
                                break
                    print('No such frame.')
