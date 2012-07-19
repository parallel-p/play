# -*- coding: utf-8 -*-
import os
from jury_state import JuryState
from player import Player
from io import BytesIO
from sys import stdout
from PIL import Image, ImageDraw, ImageFont

FRAME_SIDE = 1024
FREE_SIDE = 800
RIGHT_MARGIN = 50
SMALL_SIDE = 50
MARGIN = 20
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
    chars = ('@@', '[]', '**', 'P{:1x}')
    colors = ((5, 8, 0), (3, 2, 2), (8, 0, 2), (4, 7, 0))

    def __init__(self, players, fight=False):
        self.players = players
        self.fight = fight

    def _initialize(self, jury_state):
        self._is_initialized = True
        self._cell_side = FRAME_SIDE // jury_state.field_side

    def draw_on_the_left(self, x, players, text, color, image):
        font = ImageFont.truetype('times.ttf', 40)
        draw = ImageDraw.Draw(image)

        y = players * (SMALL_SIDE + MARGIN) - 50
        draw.text((45, y + SMALL_SIDE // 5),
                  text,
                  fill='black',
                  font=font
                  )
        x += 60
        draw.rectangle((x, y, x + SMALL_SIDE, y + SMALL_SIDE + 5),
                       fill=color
                       )
        del draw

    def paint(self, jury_state):
        '''
        Paints the state of the game;
        Returns the string --- bits of the jpeg image.
        '''
        width = FRAME_SIDE + FREE_SIDE + RIGHT_MARGIN
        height = FRAME_SIDE
        image = Image.new('RGBA',
                          (width, height),
                          'white'
                          )

        if not self._is_initialized:
            self._initialize(jury_state)

        '''
        Start drawing field
        '''
        colors = ['', 'red', 'blue', 'green', 'pink', 'black', 'yellow']

        draw = ImageDraw.Draw(image)

        x = -1
        for player in self.players:
            font = ImageFont.truetype('times.ttf', 40)
            x = max(x, font.getsize(player.author_name)[0])

        for num, player in enumerate(self.players):
            self.draw_on_the_left(x, num + 1,
                                  player.author_name,
                                  colors[num + 1], image
                                  )

        if not self.fight:
            fire_ico = image_resize(get_path(
                                    os.path.join('images', 'fire.png')),
                                    self._cell_side - 4)
            patron_ico = image_resize(get_path(
                                      os.path.join('images', 'patron.png')),
                                      self._cell_side - 4)
            player_ico = image_resize(get_path(
                                      os.path.join('images', 'player.png')),
                                      self._cell_side - 4)

            for x in range(FREE_SIDE, FREE_SIDE + FRAME_SIDE + 1,
                           self._cell_side):
                draw.line([(x, 0), (x, FRAME_SIDE)], width=LINE_WIDTH,
                          fill='grey')

            for y in range(0, FRAME_SIDE + 1, self._cell_side):
                draw.line([(FREE_SIDE, y), (FREE_SIDE + FRAME_SIDE, y)],
                          width=LINE_WIDTH, fill='grey')

            for i, row in enumerate(jury_state.field):
                for j, cell in enumerate(row):
                    x = i * self._cell_side
                    y = j * self._cell_side + FREE_SIDE
                    rectangle = (y + 1, x + 1,
                                 y + self._cell_side - 1,
                                 x + self._cell_side - 1)
                    rect = (y + 1, x + 1,
                            y + self._cell_side - 1, x + self._cell_side - 1)
                    if cell == -2:
                        draw.rectangle(rect, fill='black')
                        image.paste(fire_ico, (y + 2, x + 2), fire_ico)
                    elif cell == -1:
                        #draw.rectangle(rect, fill='orange')
                        image.paste(patron_ico, (y + 2, x + 2), patron_ico)
                    elif cell == 0:
                        pass
                    else:
                        draw.rectangle(rectangle, fill=colors[cell])
                        image.paste(player_ico, (y + 2, x + 2), player_ico)
        else:
            player_ico = image_resize(get_path(
                                      os.path.join('images', 'player.png')),
                                      width // 3)
            size = player_ico.size[0]
            rectangle = (width // 8, height // 5,
                         width // 8 + size - 5, height // 5 + size - 5)
            draw.rectangle(rectangle, fill='red')
            rectangle = (width // 8 + width // 2, height // 5,
                         width // 8 + width // 2 + size - 5,
                         height // 5 + size - 5)
            draw.rectangle(rectangle, fill='blue')
            image.paste(player_ico, (width // 8, height // 5), player_ico)
            image.paste(player_ico, (width // 8 + width // 2, height // 5),
                        player_ico)
            font = ImageFont.truetype('times.ttf', 100)
            text = 'Gunplay!'
            draw.text((int(width // 2.3), height // 3),
                      text, fill='black', font=font)
            patron_font = ImageFont.truetype('times.ttf', 70)
            draw.text((width // 4, int(height / 4 * 2.8)),
                      str(jury_state.bullets[0]), fill='black',
                      font=patron_font)
            draw.text((width // 4 + width // 2, int(height // 4 * 2.8)),
                      str(jury_state.bullets[1]), fill='black',
                      font=patron_font)
            patron_ico = image_resize(get_path('images/patron-90.png'), 80)
            image.paste(patron_ico, (int(width // 3.2),
                        int(height // 4 * 2.8)),
                        patron_ico)
            image.paste(patron_ico, (int(width // 3.2) + width // 2,
                        int(height // 4 * 2.8)),
                        patron_ico)

            if jury_state.bullets[0] == jury_state.bullets[1]:
                text = 'Draw!'
            elif jury_state.bullets[0] > jury_state.bullets[1]:
                text = '{} win!'.format(self.players[0].author_name)
            else:
                text = '{} win!'.format(self.players[1].author_name)
            draw.text((int(width // 2.5), height // 20 * 16),
                      text, fill='black', font=font)

        '''
        Finish drawing field
        '''
        del draw
        image.save("test-1.png", "PNG")
        #image.show()
        bytes = BytesIO()
        image.save(bytes, format='png')
        return bytes.getvalue()


painter = Painter([Player(None, 'Dima'), Player(None,
                  'Vasya OLLOLOLOOLOtrsgyygu')], fight=False)
side = 10
field = [[0 for i in range(side)] for j in range(side)]
field[7][3] = 1
field[7][4] = 2
field[8][8] = field[5][3] = field[3][7] = field[3][4] = field[6][6] = -1
jury_state = JuryState(side, field, [30, 17], None, None, None)
painter.paint(jury_state)
