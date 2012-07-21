import game_controller
from log import logger
import config
from bot_factory import create, is_psutil
import copy
import time
import sys


class GameSimulator:
    '''
    Class manages one game match.
    Usage:
        >> eng = GameSimulator(config, players, start_state, game_signature)
        >> eng.play()
    Examples:
    # Getting class to Bot instance
    >> game_simulator.get_move(player, player_state, serializer, deserializer)
    '''
    def __init__(self, players, start_state, game_signature):
        '''
        Constructor of class GameSimulator.
        Creates an object of the class, gets config, players list,
        jury_state and game_signature
        '''
        self._start_state = start_state
        self._game_controller = game_controller.GameController(players,
          game_signature, start_state, self)

    def _create_bots(self):
        '''
        Creates bots for each player
        '''
        self.bots = {}
        for player in self._game_controller._players:
            self.bots[player] = create()(player.command_line)
            self.bots[player].create_process()
            logger.debug('created bot \'%s\'', player.bot_name)
        logger.info('all bots created')

    def get_move(self, player, player_state, serialaizer, deserializer):
        '''
        Gets move to Bot instance
        '''
        new_move = self.bots[player].get_move(player_state,
                                              serialaizer, deserializer)
        logger.debug('bot \'%s\' made a move', player.bot_name)
        print('.', end='')
        sys.stdout.flush()
        return new_move

    def _kill_bots(self):
        '''
        Killes ALL running bots
        '''
        for bot in self.bots.values():
            bot.kill_process()
        logger.info('all bots killed')

    def report_state(self, jury_state):
        '''
        Saves jury states to array
        '''
        copied_js = copy.deepcopy(jury_state)
        self._game_controller.jury_states.append(copied_js)

    def play(self):
        '''
        Starts the game, executes master game program and updates
        game_controller, then finishes the game and kills
        all the bots.
        '''
        try:
            self._create_bots()
            start_time = time.time()
            game_master = config.GameMaster(self._game_controller, self._start_state)
            while not self._game_controller.is_finished:
                copied_js = copy.deepcopy(self._game_controller.jury_states[-1])
                try:
                    game_master.tick(copied_js)
                except:
                    logger.critical('game master was raised an '
                                    'unhandled exception, aborting')
                    self._kill_bots()
                    logger.critical('re-raising game master\'s exception')
                    raise
            end_time = time.time()
            logger.info('time spent on the game: %f sec',
                        end_time - start_time)
            return self._game_controller
        finally:
            self._kill_bots()

    def get_players(self):
        '''
        Gets players list as an list of instances
        '''
        return self._game_controller._players

    def finish_game(self, scores):
        '''
        Finishes game with `scores`
        '''
        self._game_controller.is_finished = True
        self._game_controller._scores = scores
        logger.info('game finished')
