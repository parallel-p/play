# -*- coding: utf-8 -*-


def set_color(color, print_result=False):
    '''takes a 3-tuple with codes for Background, Foreground and Style and
    returns a string with ANSI escape codes for each of them.
    Any of them can be None, in which case the respective codes will not be
    added to the string.
    If print_result is True, then it also writes these codes to stdout'''
    (back, fore, style) = color
    from sys import stdout
    CSI = '\x1b['
    #        0     1     2     3     4     5     6     7     8
    #        black blue  cyan  green mag   red   RST   white yellow
    backc = ['40', '44', '46', '42', '45', '41', '49', '47', '43']
    forec = ['30', '34', '36', '32', '35', '31', '39', '37', '33']
    #         0    1    2     3
    #         brt  dim  norm  RST
    stylec = ['1', '2', '22', '0']
    code = ''
    for param, arg in zip([backc, forec, stylec], [back, fore, style]):
        if arg is not None:
            code += (CSI + param[arg] + 'm')
    if print_result:
        stdout.write(code)
    return(code)


class Painter():

    class Cell():

        def __init__(self, val, color):
            self.value = val
            self.color = color

    def __init__(self, players, chars=('@@', '[]', '**', 'P{}'),
    colors=((5, 8, 0), (3, 2, 2), (8, 0, 2), (4, 7, 0))):
        '''This is the class constructor which optionally takes
    custom characters or colors for in-game objects in
    the following order:
    0: Burning Ground
    1: Normal Ground
    2: Shells
    3: Players
    The Player chars must be a valid format string with
    the player's number as its parameter and each of the
    colors must be a valid color tuple for the set_color function'''
        self.players = players
        if len(chars) != 4 or len(colors) != 4:
            raise Exception('Invalid parameters')
        self.chars = chars
        self.colors = colors

    def _generate_player_stats(self, players, bullets, scores, dead, dead_reason):
        statstr = '{headercolor}Players in game:{reset}\n'.format(
            headercolor=set_color((1, 8, 0)),
            reset=set_color((None, None, 3)))
        for pnum, (player, bulletn) in enumerate(zip(players, bullets)):
            player_reason = ''
            if player in dead:
                if dead_reason[player] == -1:
                    player_reason = 'made wrong move'
                elif dead_reason[player] == 0:
                    player_reason = 'destroyed by Armageddon'
                else:
                    player_reason = 'killed with bullet'
            (bgcolor, endmsg) = ((5, None, None), ' is dead ({reason}), with score {numcolor}{score:4}{textc}' ) if player in dead else ((0, None, None), ' has {numcolor}{bullets:4d}{textc} bullets        ')
            scor=scores.get(player)
            if scor is None:
                scor = 0
            statstr += ('{bkgnd}{icolor}[{player_index}]{botcolor}{player.bot_name:8s}{textc} by {authorcolor}{player.author_name:15s}{textc}' + endmsg + '{reset}\n').format(
                score=scor,
                bullets=bulletn,
                player=player,
                player_index=self.chars[3].format(pnum),
                bkgnd=set_color(bgcolor),
                icolor=set_color((None, 7, 0)),
                botcolor=set_color((None, 3, 2)),
                textc=set_color((None, 8, 2)),
                authorcolor=set_color((None, 2, None)),
                numcolor=set_color((None, 4, None)),
                reason = player_reason,
                reset=set_color((None, None, 3))
            )
        return statstr

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
            elif(self.collision_ids is not None and
                 (pos - 1) in self.collision_ids):
                cell = self.Cell(self.chars[3].format(pos - 1), self.colors[0])
            else:
                cell = self.Cell(self.chars[3].format(pos - 1), self.colors[3])
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
        player_stats = self._generate_player_stats(self.players,
                                                   jury_state.bullets,
                                                   jury_state.scores,
                                                   jury_state.dead_players,
                                                   jury_state.dead_reason)
        text_field = ''
        
        if jury_state.collision is not None:
            self.collision_ids = [self.players.index(player) for player in jury_state.collision]
        else:
            self.collision_ids = None
        cell_field = [list(self._cell_line(fc)) for fc in jury_state.field]
        for line in cell_field:
            text_field += self._generate_line(line) + '\n'
        return text_field + '\n' + player_stats
