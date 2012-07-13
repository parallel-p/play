import pickle
import os
#import engine
from game_supporting_classes import GameSignature


class Game:
    '''Starts the game, writes logs and returns results of the game'''

    def __init__(self, init_jury_state, game_info, config, players):
        self.jury_state = init_jury_state
        self.game_info = game_info
        self.result = dict()
        self.config = config
        self.players = players
        self.game_controller = None

    def _write_logs(self):
        '''writes the logs of the game'''
        path = os.path.dirname(__file__)
        path = os.path.join(path, 'logs')
        path = os.path.join(path, 'tour' + str(self.game_info.tournament_id))
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
        game_engine = engine.Engine(config, players, jury_state, game_info)
        self.game_controller = game_engine.play()
        self._write_logs()

    def get_result(self):
        '''returns results of the game'''
        return self.game_controller.players
