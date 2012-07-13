import game_controller


class GameSimulator:
    '''
    Class manages one game match.
    Usage:
        >> eng = GameSimulator(config, players, jury_state, game_signature)
        >> eng.play()
    '''
    def __init__(self, config, players, jury_state, game_signature):
        '''
        Constructor of class GameSimulator.
        Creates an object of the class, gets config, players list,
        jury_state and game_signature
        '''
        self._game_controller = game_controller.GameController(config,
                                players, game_signature, jury_state)
        self._game_master =\
             config.game_master_constructor(self._game_controller, jury_state)

    def play(self):
        '''
        Starts the game, executes master game program and updates
        game_controller, then finishes the game and kills
        all the bots.
        '''
        self._game_controller.create_bots()
        while not self._game_controller.is_finished:
            self._game_master.tick(self._game_controller)
        self._game_controller.kill_bots()
        return self._game_controller
