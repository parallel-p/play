import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

MY_DIR = os.path.abspath(os.path.dirname(__file__))

class ImageDrawTree:
    '''
    This class draw image based on `data` with results
    of the tournament.
    '''
    def draw_tree(self, data):
        def get_path(filename):
            return os.path.join(MY_DIR, filename)

        def create_game(first_line, second_line):
            '''
            Print first column with results.
            '''
            winner_line = (first_line + second_line) // 2
            draw.line((indent, first_line, indent + line_len, first_line),
                    fill='black', width=3)
            draw.line((indent, second_line, indent + line_len, second_line),
                fill='black', width=3)
            draw.line((indent + line_len, first_line, indent + line_len,
                second_line), fill='black', width=3)
            draw.line((indent + line_len, winner_line, indent + 2 * line_len,
                winner_line), fill='black', width=3)

        def set_names(first_line, second_line, players):
            '''
            Print names of the all players in the first round.
            '''
            winner_line = (first_line + second_line) // 2
            font = ImageFont.truetype(get_path('times.ttf'), 33)
            draw.text((indent, first_line - eps), players[0], fill=colors[1],
                font=font)
            draw.text((indent, second_line - eps), players[1], fill=colors[2],
                font=font)
            draw.text((indent + line_len + eps, winner_line - eps),
                players[2], fill=colors[0], font=font)

        def draw_lines(first_line, second_line, winner):
            '''
            Print other lines of tree.
            '''
            winner_line = (first_line + second_line) // 2
            draw.line((indent, winner_line, indent + line_len, winner_line),
                fill='black', width=3)    
            draw.line((indent, first_line, indent, second_line), fill='black',
                width=3)
            font = ImageFont.truetype(get_path('times.ttf'), 33)
            draw.text((indent + eps, winner_line - eps), winner,
                fill=colors[4], font=font)    
        FRAME_SIDE = len(data[0]) * 400  # based on numbers of players
        RIGHT_MARGIN = 250
        width = FRAME_SIDE + RIGHT_MARGIN
        height = FRAME_SIDE
        image = Image.new('RGBA', (width, height), 'white')
        colors = ['red', 'blue', 'green', 'pink', 'black', 'yellow']
        draw = ImageDraw.Draw(image)
        eps = 50  # height of indent before name
        line_len = 333  # length of line with name

        f_line, s_line = 100, 300 # y-coordinates of first player
        indent = 10  # indent for first players
        round_ind = [(200, 600), (400, 1200), (800, 2400)]  #other indents
        for round_id in range(len(data)):
            for game in data[round_id]:
                if round_id == 0:
                    players = [str(game[0][0]), str(game[1][0])]
                    if game[0][1] > game[1][1]:
                        players.append(str(game[0][0]))
                    else:
                        players.append(str(game[1][0]))
                    create_game(f_line, s_line)
                    set_names(f_line, s_line, players)
                    f_line = s_line + 200
                    s_line = f_line + 200
                else:
                    if game[0][1] > game[1][1]:
                        winner = str(game[0][0])
                    else:
                        winner = str(game[1][0])
                    draw_lines(f_line, s_line, winner)
                    f_line = s_line + 200 * (round_id + 1)
                    s_line = f_line + 200 * (round_id + 1)
            f_line, s_line = round_ind[round_id][0], round_ind[round_id][1]
            indent += line_len * (2 - round_id)

        image.save("results.jpeg", "JPEG")
        bytes = BytesIO()
        image.save(bytes, format='JPEG')
        return bytes.getvalue()
