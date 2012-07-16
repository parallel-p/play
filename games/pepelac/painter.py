from PIL import Image, ImageDraw, ImageFont
from jury_state import JuryState
from player import Player
from io import BytesIO

FRAME_SIDE = 1024
FREE_SIDE = 1024
RIGHT_MARGIN = 256
SMALL_SIDE = 50
MARGIN = 20


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
        self._cell_side = FRAME_SIDE / jury_state.field_side

    def draw_on_the_left(self, players, text, color, image):
        font = ImageFont.truetype('times.ttf', 30)
        draw = ImageDraw.Draw(image)

        x = 100
        y = players * (SMALL_SIDE + MARGIN)
        draw.text((0, y + SMALL_SIDE / 4),
                  text,
                  fill='black',
                  font=font
                  )
        draw.rectangle((x, y, x + SMALL_SIDE, y + SMALL_SIDE),
                       fill=color
                       )
        del draw

    def paint(self, jury_state):
        '''
        Paints the state of the game;
        Returns the string --- bits of the jpeg image.
        '''
        image = Image.new('RGBA',
                          (FRAME_SIDE + FREE_SIDE + RIGHT_MARGIN, FRAME_SIDE),
                          'white'
                          )

        if not self._is_initialized:
            self._initialize(jury_state)

        '''
        Start drawing field
        '''
        colors = ['', 'black', 'yellow', 'green', 'pink', 'red', 'blue']
        players_count = 0

        fire_ico = image_resize('fire.jpg', self._cell_side - 10)
        patron_ico = image_resize('patron.jpg', self._cell_side - 10)
        player_ico = image_resize('player.png', self._cell_side - 10)

        for i, row in enumerate(jury_state.field):
            for j, cell in enumerate(row):
                x = i * self._cell_side
                y = j * self._cell_side + FREE_SIDE
                rectangle = (y, x, y + self._cell_side, x + self._cell_side)

                draw = ImageDraw.Draw(image)

                if cell == -2:
                    draw.rectangle(rectangle, outline='black')
                    image.paste(fire_ico, (y + 5, x + 5))
                elif cell == -1:
                    draw.rectangle(rectangle, fill='purple', outline='black')
                    image.paste(patron_ico, (y + 5, x + 5))
                elif cell == 0:
                    draw.rectangle(rectangle, outline='black')
                else:
                    name = self.players[players_count].author_name
                    self.draw_on_the_left(players_count,
                                          name,
                                          colors[cell], image
                                          )
                    draw.rectangle(rectangle,
                                   fill=colors[cell],
                                   outline='black'
                                   )
                    players_count += 1
                    image.paste(player_ico, (y + 5, x + 5), player_ico)

                del draw

        '''
        Finish drawing field
        '''

        #image.save("test-1.png", "PNG") #if you want to see picture
        #image.show()
        bytes = BytesIO()
        image.save(bytes, format='png')
        return bytes.getvalue()

'''
painter = Painter()
side = 7
field = [[0 for i in range(side)] for j in range(side)]
field[0][2] = -2
field[0][3] = -2
field[0][4] = -2
field[1][3] = -1
field[2][1] = 1
field[4][3] = 2
field[3][2] = 3
field[0][0] = 4
field[4][1] = 5
field[2][3] = 6
jury_state = JuryState(side, field, None, None,
                       [Player(None, 'Dima'), Player(None, 'Vasya'),
                        Player(None, 'Alice'), Player(None, 'Nick'),
                        Player(None, 'Petr'), Player(None, 'Artur')]
                       )
painter.paint(jury_state)'''
