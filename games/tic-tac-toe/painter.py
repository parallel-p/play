from io import BytesIO


FRAME_WIDTH = 500
FRAME_HEIGHT = 1000
BORDER = 10
MARGIN = 10


class Painter:
    _is_initialized = False

    def __init__(self, players):
        pass

    def _initialize(self, jury_state):
        pass

    def paint(self, jury_state):
        pass

    def ascii_paint(self, js):
        ''' This method is used to paint in ASCII-art for using with
        ASCII visualizer (from development tools). It returns an ASCII
        string with image of the game field. '''
        return '\n'.join([' '.join([j \
            for j in js.field[i * 3:(i + 1) * 3]]) for i in range(3)])
