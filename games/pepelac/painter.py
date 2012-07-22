import os
from jury_state import JuryState
from player import Player
from sys import stdout
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

FRAME_SIDE = 1024
FREE_SIDE = 1024
RIGHT_MARGIN = 50
SMALL_SIDE = 50
MARGIN = 20
LINE_WIDTH = 1
MAX_NAME_LENGTH = 15
MY_DIR = os.path.abspath(os.path.dirname(__file__))


class NoPlayerInTheListException(Exception):
    pass


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
        self._cell_side = FRAME_SIDE // jury_state.field_side

        self._width = FRAME_SIDE + FREE_SIDE + RIGHT_MARGIN
        self._height = FRAME_SIDE

        self._fire_ico = image_resize(get_path(
                                      os.path.join('images',
                                                   'fire.png'
                                                   )
                                      ), self._cell_side - 4
                                      )
        self._patron_ico = image_resize(get_path(
                                        os.path.join('images',
                                                     'patron.png'
                                                     )
                                        ), self._cell_side - 4
                                        )
        self._player_ico = image_resize(get_path(
                                        os.path.join('images',
                                                     'player.png'
                                                     )
                                        ), self._cell_side - 4
                                        )
        self._player_ico_fight = image_resize(get_path(
                                              os.path.join('images',
                                                           'player.png'
                                                           )
                                              ), self._width // 3
                                              )
        self._patron_ico_fight = image_resize(get_path('images/patron-90.png'),
                                              80
                                              )
        self._patron_ico_left = image_resize(get_path('images/patron-90.png'),
                                             SMALL_SIDE
                                             )

    def cut_name(self, name):
        if (len(name) > MAX_NAME_LENGTH):
            name = name[:MAX_NAME_LENGTH - 3] + '...'
        return name

    def index_of_player(self, _list, player_to_find):
        if (len(_list) == 0):
            return -1
        for idx, player in enumerate(_list):
            if (player.author_name == player_to_find.author_name):
                return idx
        return -1

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

        colors = ['', 'red', 'blue', 'green', 'pink', 'black', 'yellow']

        draw = ImageDraw.Draw(image)

        if not jury_state.collision:
            '''
            Start Drawing empty table
            '''
            for x in range(FREE_SIDE, FREE_SIDE + FRAME_SIDE + 1,
                           self._cell_side):
                draw.line([(x, 0), (x, FRAME_SIDE)], width=LINE_WIDTH,
                          fill='grey')

            for y in range(0, FRAME_SIDE + 1, self._cell_side):
                draw.line([(FREE_SIDE, y), (FREE_SIDE + FRAME_SIDE, y)],
                          width=LINE_WIDTH, fill='grey')
            '''
            Finish drawing empty table
            '''

            for i, row in enumerate(jury_state.field):
                for j, cell in enumerate(row):
                    x = i * self._cell_side
                    y = j * self._cell_side + FREE_SIDE
                    rectangle = (y + 1, x + 1,
                                 y + self._cell_side - 1,
                                 x + self._cell_side - 1)
                    if cell == -2:    # this cell has been exploded
                        draw.rectangle(rectangle, fill='black')
                        image.paste(self._fire_ico,
                                    (y + 2, x + 2),
                                    self._fire_ico
                                    )
                    elif cell == -1:  # there is a bullet in this cell
                        image.paste(self._patron_ico,
                                    (y + 2, x + 2),
                                    self._patron_ico
                                    )
                    elif cell == 0:   # this cell is empty
                        pass
                    else:             # there is a player in this cell
                        draw.rectangle(rectangle, fill=colors[cell])
                        image.paste(self._player_ico,
                                    (y + 2, x + 2),
                                    self._player_ico
                                    )
        else:
            '''
            Drawing two players who have to fight
            '''
            size = self._player_ico_fight.size[0]
            rectangles = [(self._width // 8,
                           int(self._height / 4.8),
                           self._width // 8 + size - 5,
                           self._height // 5 + size - 5
                           ),
                          (self._width // 8 + self._width // 2,
                           int(self._height // 4.8),
                           self._width // 8 + self._width // 2 + size - 5,
                           self._height // 5 + size - 5
                           )
                          ]

            bullets_count = [0] * 2
            player_names = [None] * 2
            for idx, player in enumerate(jury_state.collision):
                player_names[idx] = jury_state.collision[idx].author_name
                player_id = self.index_of_player(self.players, player) + 1
                if player_id == 0:
                    message = 'There is no such player in the list'
                    raise NoPlayerInTheListException()
                color = colors[player_id]
                bullets_count[idx] = jury_state.bullets[player_id - 1]
                draw.rectangle(rectangles[idx], fill=color)

            image.paste(self._player_ico_fight,
                        (self._width // 8, int(self._height / 4.8)),
                        self._player_ico_fight
                        )
            image.paste(self._player_ico_fight,
                        (self._width // 8 + self._width // 2,
                        int(self._height / 4.8)),
                        self._player_ico_fight
                        )

            font = ImageFont.truetype(get_path('times.ttf'), 100)
            text = 'Gunplay!'

            draw.text((int(self._width / 2.3), self._height // 3),
                      text, fill='black', font=font)

            '''
            Drawing number of bullets
            '''
            patron_font = ImageFont.truetype(get_path('times.ttf'), 70)
            y = self._height // 5 + size + 10
            coordinates = [(self._width // 4, y),
                           (self._width // 4 + self._width // 2, y)
                           ]

            for idx, bullets_cnt in enumerate(bullets_count):
                draw.text(coordinates[idx],
                          str(bullets_cnt), fill='black',
                          font=patron_font
                          )

            image.paste(self._patron_ico_fight,
                        (int(self._width / 3.2), y),
                        self._patron_ico_fight
                        )
            image.paste(self._patron_ico_fight,
                        (int(self._width / 3.2) + self._width // 2, y),
                        self._patron_ico_fight
                        )

            if bullets_count[0] == bullets_count[1]:
                text = 'Draw!'
            elif bullets_count[0] > bullets_count[1]:
                text = '{} win!'.format(player_names[0])
            else:
                text = '{} win!'.format(player_names[1])
            width = font.getsize(text)[0]
            draw.text(((self._width - width) // 2 + 100,
                       self._height // 20 * 16),
                      text, fill='black', font=font
                      )

        '''
        x is maximal width of players names
        '''
        max_x = -1
        for player in self.players:
            font = ImageFont.truetype(get_path('times.ttf'), 40)
            text = self.cut_name(player.author_name)
            max_x = max(max_x,
                        font.getsize(text)[0]
                        )

        '''
        Drawing names, colors, patrons etc. on the left of picture
        '''
        for num, player in enumerate(self.players):
            x = max_x
            font = ImageFont.truetype(get_path('times.ttf'), 40)

            y = num * (SMALL_SIDE + MARGIN)
            draw.text((45, y + SMALL_SIDE // 5),
                      self.cut_name(player.author_name),
                      fill='black',
                      font=font
                      )

            x += 60
            draw.rectangle((x, y, x + SMALL_SIDE, y + SMALL_SIDE + 5),
                           fill=colors[num + 1]
                           )

            if (self.index_of_player(jury_state.dead_players, player) != -1):
                draw.text((x + 80, y + SMALL_SIDE // 5),
                          'Dead with score ' + str(jury_state.scores[player]),
                          fill='black', font=font
                          )
                continue

            x += SMALL_SIDE + 20
            patron_font = ImageFont.truetype(get_path('times.ttf'), 30)
            draw.text((x, y + SMALL_SIDE // 4),
                      str(jury_state.bullets[num]),
                      fill='black',
                      font=patron_font
                      )
            image.paste(self._patron_ico_left,
                        (x + 20, y),
                        self._patron_ico_left
                        )

        del draw

        #image.save("test-1.png", "png")
        bytes = BytesIO()
        image.save(bytes, format='png')
        return bytes.getvalue()
