import config
import tournament_stages.series as series


class Round:
    '''Manages and starts round'''
    def __init__(self, players_list, game_info):
        self._players_list = players_list
        self._games_count = len(self._players_list)
        self._jurystates_list = []
        self.games_results = {}
        self._game_info = game_info
        self._generate_series()

    def _generate_series(self):
        '''Generates series for one round'''
        # Unknown function of generator
        self._jurystates_list = config.Generator().generate_start_positions(
            self._game_info,
            len(self._players_list[0]))

    def run(self):
        '''Starts series of round'''
        for series_id in range(self._games_count):
            self._game_info.series_id = series_id
            self.series = series.Series(
                initial_jurystates=self._jurystates_list,
                signature=self._game_info,
                players_list=self._players_list[series_id])
            self.series.run()
            self.games_results.update(self.series.get_results())
