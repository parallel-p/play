class ASCIIDrawTree:
    def draw_tree(self, data):
        '''
        Returns list of strings of the tree based on the
        `data`.
        '''
        round_number = len(data)
        tree = [''] * (2 ** round_number - 1)
        final_tree = []
        shift = 1 # How much cells we jump over
        for rnum, round_id in enumerate(data):
            idx = 0 # idx is index in round_id
            for game in range(shift - 1, len(tree), shift * 2):
                tree[game] = (round_id[idx], rnum)
                idx += 1
            shift *= 2
        for idx in tree:
            separ = ' ' * 18 * idx[1] + 'Player '
            player1 = separ + str(idx[0][0][0]) + ': ' + str(idx[0][0][1]) + ' points'
            player2 = separ + str(idx[0][1][0]) + ': ' + str(idx[0][1][1]) + ' points'
            game_result = player1 + '\n' + player2
            final_tree.append(game_result)
        return final_tree