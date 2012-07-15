import game_controller
from log import logger
import config
import bot
import copy


class GameSimulator:
    '''
    Class manages one game match.
    Usage:
        >> eng = GameSimulator(config, players, jury_state, game_signature)
        >> eng.play()
    Examples:
    # Getting class to Bot instance
    >> game_controller.get_move(player, player_state, serializer, deserializer)
    # Creating and killing ALL bots
    >> game_controller.create_bots()
    >> game_controller.kill_bots()
    '''
    def __init__(self, players, jury_state, game_signature):
        '''
        Constructor of class GameSimulator.
        Creates an object of the class, gets config, players list,
        jury_state and game_signature
        '''
        self._game_controller = game_controller.GameController(players,
                                    game_signature, jury_state)
        self._game_master = config.GameMaster(self, jury_state)
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

    def get_move(self, player, player_state, serialaizer, deserializer):
        '''
        Gets move to Bot instance
        '''
        new_move = self.bots[player].get_move(player_state,
                                              serialaizer, deserializer)
        logger.info('bot "%s" made a move', player.bot_name)
        return new_move

    def kill_bots(self):
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
        self.create_bots()
        while not self._game_controller.is_finished:
            copied_js = copy.deepcopy(self._game_controller.jury_states[-1])
            self._game_master.tick(copied_js)
        self.kill_bots()
        return self._game_controller

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