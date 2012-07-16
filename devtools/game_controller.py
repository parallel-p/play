from log import logger


class GameNotFinishedException(Exception):
    pass


class GameController:
    '''
    GameController is a class, which controls game manager.
    Usage:
    >> game_controller = GameController(config, players, signature, jury_state)
    Examples:
    # Saving jury states to array
    >> game_controller.report_state(jury_state)
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

    def finish_game(self, scores):
        '''
        Finishes game with `scores`
        '''
        self.is_finished = True
        self._scores = scores
        logger.info('game finished')

    def get_scores(self):
        '''
        Gets scores of finished game
        '''
        if not self.is_finished:
            raise GameNotFinishedException()
        return self._scores

    def __lt__(self, other):
        return self.signature < other.signature
