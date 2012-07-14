from PIL import Image, ImageDraw, ImageFont
from jury_state import JuryState
from player import Player
from io import BytesIO

FRAME_SIDE = 1024
FREE_SIDE = 1024
RIGHT_MARGIN = 256
SMALL_SIDE = 50
MARGIN = 20


class Painter:
    _is_initialized = False

    def _initialize(self, jury_state):
        self._is_initialized = True
        self._cell_side = FRAME_SIDE / jury_state.field_side

    def draw_on_the_left(self, players, text, color, image):
        font = ImageFont.truetype('times.ttf', 30)
        draw = ImageDraw.Draw(image)

        x = 100
        y = players * (SMALL_SIDE + MARGIN)
        draw.text((0, y + SMALL_SIDE / 4),
                  text + ' - ',
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
        image = Image.new('RGB',
                          (FRAME_SIDE + FREE_SIDE + RIGHT_MARGIN, FRAME_SIDE),
                          (255, 255, 255)
                          )
        if not self._is_initialized:
            self._initialize(jury_state)

        '''
        Start drawing field
        '''
        colors = ['', 'black', 'yellow', 'green', 'pink', 'red', 'blue']
        self.draw_on_the_left(0, 'Bullet', 'purple', image)
        players = 1

        for i, row in enumerate(jury_state.field):
            for j, cell in enumerate(row):
                x = i * self._cell_side
                y = j * self._cell_side + FREE_SIDE
                rectangle = (y, x, y + self._cell_side, x + self._cell_side)

                if cell == -2:
                    continue

                draw = ImageDraw.Draw(image)

                if cell == -1:
                    draw.rectangle(rectangle, fill='purple', outline='black')
                elif cell == 0:
                    draw.rectangle(rectangle, outline='black')
                else:
                    name = players[players - 1].author_name
                    self.draw_on_the_left(players,
                                          jury_state.name + ' - ',
                                          colors[cell], image
                                          )
                    draw.rectangle(rectangle,
                                   fill=colors[cell],
                                   outline='black'
                                   )
                    players += 1

                del draw

        '''
        Finish drawing field
        '''

        #image.save("test.png", "PNG") #if you want to see picture
        bytes = BytesIO()
        image.save(bytes, format='png')
        return bytes.getvalue()

'''painter = Painter()
side = 20
field = [[0 for i in range(side)] for j in range(side)]
field[0][2] = -2
field[0][3] = -2
field[0][4] = -2
field[1][3] = -1
field[2][1] = 1
field[4][3] = 2
field[5][7] = 3
field[7][2] = 4
field[6][8] = 5
field[8][11] = 6
jury_state = JuryState(side, field, None, None,
                       [Player(None, 'Dima'), Player(None, 'Vasya'),
                        Player(None, 'Vasya'), Player(None, 'Vasya'),
                        Player(None, 'Vasya'), Player(None, 'Vasya')]
                       )
painter.paint(jury_state)'''
