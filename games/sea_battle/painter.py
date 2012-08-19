from io import BytesIO
import os
from PIL import Image, ImageDraw, ImageFont

FRAME_SIDE = 1024
MARGIN = 256
Y_MARGIN = 128
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

    def __init__(self, players):
        self._players = players

    def _initialize(self, jury_state):
        self._is_initialized = True
        self._cell_side = FRAME_SIDE // jury_state.field_side
        self._width = 2 * FRAME_SIDE + MARGIN
        self._height = FRAME_SIDE + Y_MARGIN
        self._fire_ico = image_resize(get_path(
                                      os.path.join('images',
                                                   'fire.png'
                                                   )
                                      ), self._cell_side
                                      )

    def cut_name(self, name):
        if (len(name) > MAX_NAME_LENGTH):
            name = name[:MAX_NAME_LENGTH - 3] + '...'
        return name

    def draw_fire(self, image, x, y):
        image.paste(self._fire_ico, (x, y), self._fire_ico)

    def draw_empty_tables(self, draw):
        for x in range(0, FRAME_SIDE + 1, self._cell_side):
            draw.line([(x, Y_MARGIN), (x, FRAME_SIDE + Y_MARGIN)],
                      width=LINE_WIDTH, fill='grey')
            draw.line([(x + FRAME_SIDE + MARGIN, Y_MARGIN),
                       (x + FRAME_SIDE + MARGIN, FRAME_SIDE + Y_MARGIN)],
                      width=LINE_WIDTH, fill='grey')

        for y in range(Y_MARGIN, Y_MARGIN + FRAME_SIDE + 1, self._cell_side):
            draw.line([(0, y), (FRAME_SIDE, y)], width=LINE_WIDTH, fill='grey')
            draw.line([(FRAME_SIDE + MARGIN, y), (2 * FRAME_SIDE + MARGIN, y)],
                      width=LINE_WIDTH, fill='grey')

    def draw_ship(self, image, draw, ship, js, over_x, idx):
        for cell in ship:
            (x, y) = (cell[0], cell[1])
            coordinates = (over_x + y * self._cell_side,
                           x * self._cell_side + Y_MARGIN,
                           over_x + (y + 1) * self._cell_side,
                           (x + 1) * self._cell_side + Y_MARGIN
                           )
            if js.start_fields[idx][x][y] > 0 and js.fields[idx][x][y] == -1:
                self.draw_fire(image, coordinates[0], coordinates[1])
            else:
                draw.rectangle(coordinates, fill='black')

    '''def draw_pictures(self, image, draw, start_field, field, over_x):
        for i, row in enumerate(field):
            for j, cell in enumerate(row):
                (x, y) = (j * self._cell_side + over_x,
                          i * self._cell_side + Y_MARGIN)
                if start_field[i][j] > 0 and cell == -1:
                    self.draw_fire(image, x, y)
                elif cell > 0:
                    draw.rectangle((x, y, x + self._cell_side,
                                   y + self._cell_side), fill='black')
                elif cell == -1:
                    x += self._cell_side // 2
                    y += self._cell_side // 2
                    draw.ellipse((x - 5, y - 5, x + 5,
                                 y + 5), fill='black')'''

    def draw_pictures(self, image, draw, jury_state, idx, over_x):
        for i, row in enumerate(jury_state.fields[idx]):
            for j, cell in enumerate(row):
                (x, y) = (j * self._cell_side + over_x,
                          i * self._cell_side + Y_MARGIN)
                if cell == -1:
                    x += self._cell_side // 2
                    y += self._cell_side // 2
                    draw.ellipse((x - 5, y - 5, x + 5,
                                 y + 5), fill='black')
        for ship in jury_state.ships[idx]:
            self.draw_ship(image, draw, ship, jury_state, over_x, idx)

    def draw_player_on_the_up(self, font, draw, over_x, idx):
        text = 'Field of ' + self._players[idx].author_name
        if font.getsize(text)[0] > FRAME_SIDE:
            text = 'Field of ' + self.cut_name(self._players[idx].author_name)
        x = over_x + (FRAME_SIDE - font.getsize(text)[0]) // 2
        y = (Y_MARGIN - font.getsize(text)[1]) // 2
        draw.text((x, y), text, fill='black', font=font)

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
        over_x = FRAME_SIDE + MARGIN

        if jury_state.winner is None:
            self.draw_empty_tables(draw)
            self.draw_pictures(image, draw, jury_state, 0, 0)
            self.draw_pictures(image, draw, jury_state, 1, over_x)

            font = ImageFont.truetype(get_path(
                                      os.path.join('fonts',
                                                   'times.ttf'
                                                   )
                                      ), 60)
            self.draw_player_on_the_up(font, draw, 0, 0)
            self.draw_player_on_the_up(font, draw, over_x, 1)
        else:
            text_size = 500
            font = ImageFont.truetype(get_path(
                                      os.path.join('fonts',
                                                   'times.ttf'
                                                   )
                                      ), text_size)
            idx = 0
            if self._players[1].author_name == jury_state.winner.author_name:
                idx = 1
            text = jury_state.winner.author_name + ' WIN'
            self.draw_winner(font, draw, text, text_size)

        del draw

        image.save('test.jpeg', 'jpeg')  # if you want to save picture in file
        bytes = BytesIO()
        image.save(bytes, format='jpeg')
        return bytes.getvalue()
