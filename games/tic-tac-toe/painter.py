from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os


FRAME_SIDE = 1024
FREE_SIDE = 1024
RIGHT_MARGIN = 256
LINE_WIDTH = 1
MY_DIR = os.path.abspath(os.path.dirname(__file__))

def get_path(filename):
    return os.path.join(MY_DIR, filename)


def image_resize(path, output_weight):
    image = Image.open(path)
    if image.mode not in ('L', 'RGB', 'RGBA'):
        image = image.convert('RGB')
    return image.resize((output_weight, output_weight), Image.ANTIALIAS)


class Painter:
    _is_initialized = False

    def __init__(self, players):
        self.players = players

    def _initialize(self, jury_state):
        self._is_initialized = True
        self._cell_side = FRAME_SIDE // 3
        self._width = FRAME_SIDE + FREE_SIDE + RIGHT_MARGIN
        self._height = FRAME_SIDE

        self._cross_ico = image_resize(get_path(
                                      os.path.join('images',
                                                   'cross.png'
                                                   )
                                      ), self._cell_side - 4
                                      )
        self._toe_ico = image_resize(get_path(
                                      os.path.join('images',
                                                   'toe.png'
                                                   )
                                      ), self._cell_side - 4
                                      )

    def cut_name(self, name):
        if (len(name) > MAX_NAME_LENGTH):
            name = name[:MAX_NAME_LENGTH - 3] + '...'
        return name

    def draw_table(self, draw):
        for x in range(FREE_SIDE, FREE_SIDE + FRAME_SIDE + 1,
                       self._cell_side):
            draw.line([(x, 0), (x, FRAME_SIDE)], width=LINE_WIDTH,
                      fill='grey')

        for y in range(0, FRAME_SIDE + 1, self._cell_side):
            draw.line([(FREE_SIDE, y), (FREE_SIDE + FRAME_SIDE, y)],
                      width=LINE_WIDTH, fill='grey')

    def paint(self, jury_state):
        '''
        Paints the state of the game;
        Returns the string --- bits of the jpeg image.
        '''
        if not self._is_initialized:
            self._initialize(jury_state)

        image = Image.new('RGBA',
                          (self._width, self._height),
                          'white'
                          )
        draw = ImageDraw.Draw(image)
        self.draw_table(draw)
        
        for idx, element in enumerate(jury_state.field):
            x = (idx % 3) * self._cell_side + FREE_SIDE
            y = (idx // 3) * self._cell_side
            if element == 'X':
                image.paste(self._cross_ico,
                            (x + 2, y + 2),
                            self._cross_ico
                            )
            if element == 'O':
                image.paste(self._toe_ico,
                            (x + 2, y + 2),
                            self._toe_ico
                            )
        
        del draw

        image.save('test.jpeg', 'jpeg') #if you want to save picture in file
        bytes = BytesIO()
        image.save(bytes, format='jpeg')
        return bytes.getvalue()
