from log import logger
import config


class GameNotFinishedException(Exception):
    pass


class GameController:
    '''
    GameController is a class, which controls game manager.
    Usage:
    >> game_controller = GameController(config, players, signature, jury_state)
    Examples:
    # Getting class to Bot instance
    >> game_controller.get_move(player, player_state, serializer, deserializer)
    # Saving jury states to array
    >> game_controller.report_state(jury_state)
    # Creating and killing ALL bots
    >> game_controller.create_bots()
    >> game_controller.kill_bots()
    # Getting players
    >> list_of_players = game_controller.get_players()
    # Getting scores
    >> dict_of_scores = game_controller.get_scores()
    '''
    def __init__(self, players, signature, jury_state):
        '''
        Constructor of class. Creating jury states array,
        initializing base variables
        '''
        self._players = players
        self.signature = signature
        self.jury_states = [jury_state]
        self.is_finished = False

    def get_move(self, player, player_state, serialaizer, deserializer):
        '''
        Gets move to Bot instance
        '''
        new_move = player.get_move(player_state,
                                              serialaizer, deserializer)
        logger.info('bot "%s" made a move', player.bot_name)
        return new_move

    def report_state(self, jury_state):
        '''
        Saves jury states to array
        '''
        self.jury_states.append(jury_state)

    def finish_game(self, scores):
        '''
        Finishes game with `scores`
        '''
        self.is_finished = True
        self._scores = scores
        logger.info('game finished')

    def get_players(self):
        '''
        Gets players list as an list of instances
        '''
        return self._players

    def get_scores(self):
        '''
        Gets scores of finished game
        '''
        if not self.is_finished:
            raise GameNotFinishedException()
        return self._scores

    def __lt__(self, other):
        return self.signature < other.signature
