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
    def _dpc(self, n):
        return 'P{0:1x}'.format(n)

    class Cell():

        def __init__(self, val, color):
            self.value = val
            self.color = color

    def __init__(self, players, chars=None, colors=None):
        '''This is the class constructor which optionally takes
    custom characters or colors for in-game objects in
    the following order:
    0: Burning Ground
    1: Normal Ground
    2: Shells
    3: Players
    The chars[3] must be a callable which takes the player's number as
    its parameter and returns the string which the player will be marked with.
    Each of the colors must be a valid color tuple for the set_color function.
    Note that if apainter_chars and/or apainter_colors values are set in the
    config file, the class will use them instead of the default ones.
    the defaults are:
    charred earth: yellow `@@`      on red;
    normal earth : cyan   `[]`      on green;
    bullets      : black  `**`      on yellow;
    players      : white  `P{0:1x}`.format(number-of-player) on magenta.'''
        import config
        default_chars = ('@@', '[]', '**', self._dpc),
        default_colors = ((5, 8, 0), (3, 2, 2), (8, 0, 2), (4, 7, 0))
        if chars is None:
            try:
                chars = config.apainter_chars
            except AttributeError:
                chars = default_chars

        if colors is None:
            try:
                colors = config.apainter_colors
            except AttributeError:
                colors = default_colors

        self.players = players
        if len(chars) != 4 or len(colors) != 4:
            raise Exception('Invalid parameters')
        try:
            chars[3](0)
        except TypeError:
            raise Exception('chars[3] must be callable')
        self.chars = chars
        self.colors = colors

    def _generate_player_stats(self, players, bullets, scores, dead, dead_reasons):
        statstr = '{headercolor}Players in game:{reset}\n'.format(
            headercolor=set_color((1, 8, 0)),
            reset=set_color((None, None, 3)))
        for pnum, (player, bulletn) in enumerate(zip(players, bullets)):
            why_dead = ''
            if player in dead:
                if dead_reasons[player] == 1:
                    why_dead = 'killed in fight'
                elif dead_reasons[player] == -2:
                    why_dead = 'did something illegal'
                elif dead_reasons[player] == -1:
                    why_dead = 'stepped somewhere wrong'
                elif dead_reasons[player] == 0:
                    why_dead = 'burnt in Armageddon'
                else:
                    why_dead = dead_reasons[player]
            (bgcolor, endmsg) = ((5, None, None), ' is dead ({numcolor} {reason:25}{textc}), with score {numcolor}{score:4}{textc} ') if player in dead else ((0, None, None), ' has {numcolor}{bullets:4d}{textc} bullets   ' + ' ' * 35)
            scor = scores.get(player)
            if scor is None:
                scor = 0
            statstr += ('{bkgnd}{icolor}[{player_index}]{botcolor}{player.bot_name:15s}{textc} by {authorcolor}{player.author_name:20s}{textc}' + endmsg + '{reset}\n').format(
                score=scor,
                bullets=bulletn,
                player=player,
                player_index=self.chars[3](pnum),
                bkgnd=set_color(bgcolor),
                icolor=set_color((None, 7, 0)),
                botcolor=set_color((None, 3, 2)),
                textc=set_color((None, 8, 2)),
                authorcolor=set_color((None, 2, None)),
                numcolor=set_color((None, 4, None)),
                reason=why_dead,
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
            else:
                if(self.collision_ids is not None and
                (pos - 1) in self.collision_ids):
                    pcolor = self.colors[0]
                else:
                    pcolor = self.colors[3]
                cell = self.Cell(self.chars[3](pos - 1), pcolor)

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
                                                   jury_state.dead_reasons)
        text_field = ''

        if jury_state.collision is not None:
            self.collision_ids = [self.players.index(player) for player in jury_state.collision]
        else:
            self.collision_ids = None
        cell_field = [list(self._cell_line(fc)) for fc in jury_state.field]
        for line in cell_field:
            text_field += self._generate_line(line) + '\n'
        return text_field + '\n' + player_stats
