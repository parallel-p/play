import pickle
import os
import shutil
from tournament_stages.game_signature import GameSignature
from game_simulator import GameSimulator
from log import logger


class Game:
    '''Starts the game, writes logs and returns results of the game'''

    def __init__(self, init_jury_state, game_info, players):
        self.jury_state = init_jury_state
        self.game_info = game_info
        self.result = dict()
        self.players = players
        self.game_controller = None

    def _write_logs(self):
        '''writes the logs of the game'''
        path = os.path.dirname(__file__)
        path = os.path.join(path,  '..', 'logs')
        path = os.path.normpath(path)
        path = os.path.join(path, 'tournament' +
                            str(self.game_info.tournament_id))
        if (os.path.exists(path) == 0):
            os.makedirs(path)
        filename = str(self.game_info.round_id) + '-' +\
            str(self.game_info.series_id) + '-' +\
            str(self.game_info.game_id) + '.jstate'
        path = os.path.join(path, filename)
        log_file = open(path, 'wb')
        pickle.dump(self.game_controller, log_file)
        log_file.close()

    def run_engine(self):
        '''launches the engine'''
        logger.info('running game #%d', self.game_info.game_id)
        logger.info('launching engine')
        game_engine = GameSimulator(self.players, self.jury_state,
                                    self.game_info)
        logger.info('starting game')
        self.game_controller = game_engine.play()
        logger.info('writing logs')
        logger.info('game #%d finished', self.game_info.game_id)
        self._write_logs()

    def get_results(self):
        '''returns results of the game'''
        return self.game_controller.get_scores()
