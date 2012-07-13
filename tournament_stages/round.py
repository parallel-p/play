import generator
import series


class Round:
    '''Manages and starts round'''
    def __init__(self, players_list, game_info, config):
        self._players_list = players_list
        self._games_count = len(self._players_list)
        self._jurystates_list = []
        self.games_results = {}
        self._game_info = game_info
        self._config = config

    def generate_series(self):
        '''Generates series for one round'''
        # Unknown function of generator
        self._jurystates_list = generator.Generator().generate_start_positions(
            self._game_info,
            len(self._players_list[0]))

    def run(self):
        '''Starts series of round'''
        for series_id, jurystates in enumerate(self._jurystates_list):
            self._game_info.series_id = series_id
            self.series = series.Series(
                initial_jurystates_list=jurystates,
                signature=self._game_info,
                players_list=self._players_list[series_id],
                config=self._config)
            self.series.run()
            self.games_results.update(self.series.get_results())
