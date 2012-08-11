from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os


FRAME_SIDE = 1024
FREE_SIDE = 1024
RIGHT_MARGIN = 256
Y_MARGIN = 20
LINE_WIDTH = 3
MAX_NAME_LENGTH = 15
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
    _symbols = ['X', 'O']
    _lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
              [0, 3, 6], [1, 4, 7], [2, 5, 8],
              [0, 4, 8], [2, 4, 6]]

    def __init__(self, players):
        self.players = players

    def _initialize(self, jury_state):
        self._is_initialized = True
        self._cell_side = FRAME_SIDE // 3
        self._width = FRAME_SIDE + FREE_SIDE + RIGHT_MARGIN
        self._height = FRAME_SIDE

    def cut_name(self, name):
        if (len(name) > MAX_NAME_LENGTH):
            name = name[:MAX_NAME_LENGTH - 3] + '...'
        return name

    def draw_cross(self, draw, x, y):
        draw.line([(x, y), (x + self._cell_side, y + self._cell_side)],
                  fill='black', width=LINE_WIDTH
                  )
        draw.line([(x + self._cell_side, y), (x, y + self._cell_side)],
                  fill='black', width=LINE_WIDTH
                  )

    def draw_toe(self, draw, x, y):
        for i in range(5):
            draw.ellipse((x + i, y + i,
                          x + self._cell_side - i, y + self._cell_side - i),
                         outline='black'
                         )

    def draw_empty_table(self, draw):
        for x in range(FREE_SIDE, FREE_SIDE + FRAME_SIDE + 1,
                       self._cell_side):
            draw.line([(x, 0), (x, FRAME_SIDE)], width=LINE_WIDTH,
                      fill='grey')

        for y in range(0, FRAME_SIDE + 1, self._cell_side):
            draw.line([(FREE_SIDE, y), (FREE_SIDE + FRAME_SIDE, y)],
                      width=LINE_WIDTH, fill='grey')

    def get_coordinates(self, num):
        return ((num % 3) * self._cell_side + FREE_SIDE,
                (num // 3) * self._cell_side
                )

    def draw_pictures(self, image, draw, field):
        for idx, element in enumerate(field):
            (x, y) = self.get_coordinates(idx)
            if element == 'X':
                self.draw_cross(draw, x, y)
            if element == 'O':
                self.draw_toe(draw, x, y)

    def draw_player_on_the_left(self, font, draw, idx):
        y = (Y_MARGIN + self._letter_height) * idx
        draw.text((0, y),
                  self._symbols[idx] + ': ',
                  fill='black', font=font
                  )
        x = font.getsize('X: ')[0]
        draw.text((x, y),
                  self.cut_name(self.players[idx].author_name),
                  fill='black', font=font
                  )

    def draw_winner(self, font, draw, text, text_size):
        while (font.getsize(text)[0] > self._width):
            font = ImageFont.truetype(get_path(
                                      os.path.join('fonts',
                                                   'times.ttf'
                                                   )
                                      ), text_size - 10
                                      )
            text_size -= 10
        (width, height) = font.getsize(text)
        x = (self._width - width) // 2
        y = (self._height - height) // 2
        draw.text((x, y), text, fill='black', font=font)

    def draw_winner_line(self, draw, idx):
        for cell in self._lines[idx]:
            (x, y) = self.get_coordinates(cell)
            draw.rectangle((x, y, x + self._cell_side, y + self._cell_side),
                           fill='red', outline='black'
                           )

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

        if jury_state.winner is None:
            self.draw_empty_table(draw)
            if jury_state.line != -1:
                self.draw_winner_line(draw, jury_state.line)
            self.draw_pictures(image, draw, jury_state.field)

            font = ImageFont.truetype(get_path(
                                      os.path.join('fonts',
                                                   'times.ttf'
                                                   )
                                      ), 60)
            self._letter_height = font.getsize('A')[1]
            for idx, player in enumerate(self.players):
                self.draw_player_on_the_left(font, draw, idx)
        else:
            text_size = 500
            font = ImageFont.truetype(get_path(
                                      os.path.join('fonts',
                                                   'times.ttf'
                                                   )
                                      ), text_size)
            idx = 0
            if self.players[1].author_name == jury_state.winner.author_name:
                idx = 1
            text = jury_state.winner.author_name +\
                '(' + self._symbols[idx] + ') WIN'
            self.draw_winner(font, draw, text, text_size)

        del draw

        image.save('test.jpeg', 'jpeg')  # if you want to save picture in file
        bytes = BytesIO()
        image.save(bytes, format='jpeg')
        return bytes.getvalue()
