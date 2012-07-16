# -*- coding: utf-8 -*-

FRAME_SIDE = 1024
FREE_SIDE = 1024
RIGHT_MARGIN = 256
SMALL_SIDE = 50
MARGIN = 20


def set_color(color, print_result=False):
    '''takes a 3-tuple with codes for Background, Foreground and Style and
    returns a string with ANSI escape codes for each of them.
    Any of them can be None, in which case the respective codes will not be
    added to the string.
    If print_result is True, then it also writes these codes to stdout'''
    (back, fore, style) = color
    from sys import stdout
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
    chars=('@@', '[]', '**', 'P{:1x}')
    colors=((5, 8, 0), (3, 2, 2), (8, 0, 2), (4, 7, 0))

    class Cell():

        def __init__(self, val, color):
            self.value = val
            self.color = color

    def __init__(self, players):
        self.players = players

    def _initialize(self, jury_state):
        from PIL import Image, ImageDraw, ImageFont
        from jury_state import JuryState
        from player import Player
        from io import BytesIO
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
        prev_color = (None, None, 3) # total reset
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

        fire_ico = image_resize('images/fire.jpg', self._cell_side - 10)
        patron_ico = image_resize('images/patron.jpg', self._cell_side - 10)
        player_ico = image_resize('images/player.png', self._cell_side - 10)

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
