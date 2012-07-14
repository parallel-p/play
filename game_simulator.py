import game_controller
from log import logger
import config
import bot


class GameSimulator:
    '''
    Class manages one game match.
    Usage:
        >> eng = GameSimulator(config, players, jury_state, game_signature)
        >> eng.play()
    '''
    def __init__(self, players, jury_state, game_signature):
        '''
        Constructor of class GameSimulator.
        Creates an object of the class, gets config, players list,
        jury_state and game_signature
        '''
        self._game_controller = game_controller.GameController(players,
                                    game_signature, jury_state)
        self._game_master = config.GameMaster(self._game_controller,
                                              jury_state)
        self.bots = {}

    def create_bots(self):
        '''
        Creates bots for each player
        '''
        for player in self._game_controller._players:
            self.bots[player] = bot.Bot(player.command_line)
            self.bots[player].create_process()
            logger.debug('created bot "%s"', player.bot_name)
        logger.info('all bots created')

    def kill_bots(self):
        '''
        Killes ALL running bots
        '''
        for bot in self.bots.values():
            bot.kill_process()
        logger.info('all bots killed')

    def play(self):
        '''
        Starts the game, executes master game program and updates
        game_controller, then finishes the game and kills
        all the bots.
        '''
        self.create_bots()
        while not self._game_controller.is_finished:
            self._game_master.tick(self._game_controller.jury_states[-1])
        self.kill_bots()
        return self._game_controller
