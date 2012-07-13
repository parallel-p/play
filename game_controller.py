import bot
from log import logger


class GameController:
    '''

    GameController is a class, which controls game manager.
    Usage:
    >> game_controller = GameController(config, players, signature, jury_state)
    Examples:
    # Getting class to Bot instance
    >> game_controller.get_move(player, p_state, deserializer)
    # Saving jury states to array
    >> game_controller.report_state(jury_state)
    # Creating and killing ALL bots
    >> game_controller.create_bots()
    >> game_controller.kill_bots()
    # Getting players
    >> list_of_players = game_controller.get_players()
    '''
    def __init__(self, config, players, signature, jury_state):
        '''
        Constructor of class. Creating jury states array,
        initializing base variables
        '''
        self.config = config
        self._players = players
        self.signature = signature
        self.jury_states = [jury_state]
        self.is_finished = 0
        self.bots = {}

    def get_move(self, player, player_state, serialaizer, deserializer):
        '''
        Gets move to Bot instance
        '''
        new_move = self.bots[player].get_move(player_state,
                                              serialaizer, deserializer)
        logger.info('bot "%s" made a move', player.bot_name)
        return new_move

    def report_state(self, jury_state):
        '''
        Saves jury states to array
        '''
        self.jury_states.append(jury_state)

    def finish_game(self):
        '''
        Finishes game
        '''
        self.kill_bots()
        logger.info('game finished')

    def get_players(self):
        '''
        Get's players list as an list of instances
        '''
        return self._players

    def create_bots(self):
        '''
        Creates bots for each player
        '''
        for player in self._players:
            self.bots[player] = bot.Bot(player.command_line, self.config)
            logger.debug('created bot "%s"', player.bot_name)
            logger.info('all bots created')

    def kill_bots(self):
        '''
        Killes ALL running bots
        '''
        for bot in self.bots:
            bot.kill_process()
        logger.info('all bots killed')

    def __lt__(self, other):
        return self.signature < other.signature
