import os
from jury_state import JuryState
from player import Player
from io import BytesIO
from sys import stdout

try:
    import PIL
except:
    pass
finally:
    from PIL import Image, ImageDraw, ImageFont


FRAME_SIDE = 1024
FREE_SIDE = 512
RIGHT_MARGIN = 50
SMALL_SIDE = 50
MARGIN = 20
LINE_WIDTH = 1
MY_DIR = os.path.abspath(os.path.dirname(__file__))


def get_path(filename):
    return os.path.join(MY_DIR, filename)


def set_color(color, print_result=False):
    '''takes a 3-tuple with codes for Background, Foreground and Style and
    returns a string with ANSI escape codes for each of them.
    Any of them can be None, in which case the respective codes will not be
    added to the string.
    If print_result is True, then it also writes these codes to stdout'''
    (back, fore, style) = color
    CSI = '\x1b['
    backc = ['40', '44', '46', '42', '45', '41', '49', '47', '43']
    forec = ['30', '34', '36', '32', '35', '31', '39', '37', '33']
    stylec = ['1', '2', '22', '0']
    code = ''
    for param, arg in zip([backc, forec, stylec], [back, fore, style]):
        if arg is not None:
            code += (CSI + param[arg] + 'm')
    if print_result:
        stdout.write(code)
    return(code)


def image_resize(path, output_weight):
    image = Image.open(path)
    if image.mode not in ('L', 'RGB', 'RGBA'):
        image = image.convert('RGB')
    return image.resize((output_weight, output_weight), Image.ANTIALIAS)


class Painter:
    _is_initialized = False
    chars = ('@@', '[]', '**', 'P{:1x}')
    colors = ((5, 8, 0), (3, 2, 2), (8, 0, 2), (4, 7, 0))

    class Cell():

        def __init__(self, val, color):
            self.value = val
            self.color = color

    def __init__(self, players, fight=False):
        self.players = players
        self.fight = fight

    def _initialize(self, jury_state):
        self._is_initialized = True
        self._cell_side = FRAME_SIDE // jury_state.field_side

    def draw_on_the_left(self, players, text, color, image):
        font = ImageFont.truetype('times.ttf', 40)
        draw = ImageDraw.Draw(image)

        x = 145
        y = players * (SMALL_SIDE + MARGIN) + 45
        draw.text((45, y + SMALL_SIDE // 5),
                  text,
                  fill='black',
                  font=font
                  )
        draw.rectangle((x, y, x + SMALL_SIDE, y + SMALL_SIDE),
                       fill=color
                       )
        del draw

    def _cell_line(self, line):
        out = []
        for pos in line:
            if pos == -2:
                cell = self.Cell(self.chars[0], self.colors[0])
                # default: bright yellow '@@' on red
            elif pos == 0:
                cell = self.Cell(self.chars[1], self.colors[1])
                # default: cyan '[]' on green
            elif pos == -1:
                cell = self.Cell(self.chars[2], self.colors[2])
                # default: black '**' on yellow
            else:
                cell = self.Cell(self.chars[3].format(pos), self.colors[3])
                # default: bright white 'P{hex number of player}' on magenta
            out.append(cell)
        return out

    def _generate_line(self, cell_line):
        prev_color = (None, None, 3)  # total reset
        text_line = ''
        for cell in cell_line:
            # if the color of this cell is the same as
            #the previous one's, we need not change it
            if prev_color != cell.color:
                text_line += set_color(cell.color, False)
            text_line += cell.value
            prev_color = cell.color
        # reset the color in case this is the last line
        text_line += set_color((None, None, 3), False)
        return text_line

    def ascii_paint(self, jury_state):
        text_field = ''
        cell_field = [list(self._cell_line(fc)) for fc in jury_state.field]
        for line in cell_field:
            text_field += self._generate_line(line) + '\n'
        return text_field

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

        for num, player in enumerate(self.players):
            self.draw_on_the_left(num + 1,
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
            image.paste(patron_ico, (int(width // 3.2), int(height // 4 * 2.8)),
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
            draw.text((width // 3, height // 20),
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


painter = Painter([Player(None, 'Dima'), Player(None, 'Vasya')], fight=False)
side = 10
field = [[0 for i in range(side)] for j in range(side)]
field[7][3] = 1
field[7][4] = 2
field[8][8] = field[5][3] = field[3][7] = field[3][4] = field[6][6] = -1
jury_state = JuryState(side, field, [30, 17], None, None, None)
painter.paint(jury_state)
