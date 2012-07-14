class ASCIIDrawTree:
    def draw_tree(self, data):
        '''
        Returns list of strings of the tree based on the
        `data`.
        '''
        tree = []
        shift = 2
        for round_id in data:
            current_level = [''] * (2 * len(data[0]) - 1)
            for game in range((shift - 1) // 2, len(round_id), shift):
                
        return tree
