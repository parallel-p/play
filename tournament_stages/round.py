import config
import tournament_stages.series as series
from log import logger


class Round:
    '''Manages and starts round'''
    def __init__(self, players_list, game_info):
        self._players_list = players_list
        self._jurystates_list = []
        self.games_results = {}
        self._game_info = game_info
        self._generate_series()

    def _generate_series(self):
        '''Generates series for one round'''
        self._jurystates_list = list(
            config.Generator().generate_start_positions(self._game_info,
                len(self._players_list[0])))

    def run(self):
        '''Starts series of round'''
        logger.info('running round #{}'.format(self._game_info.round_id))

        for series_id in range(len(self._players_list)):
            self._game_info.series_id = series_id
            self.series = series.Series(
                initial_jurystates=self._jurystates_list,
                signature=self._game_info,
                players_list=self._players_list[series_id])
            self.series.run()
            self.games_results.update(self.series.get_results())
        logger.info('running round #{}'.format(self._game_info.round_id))
