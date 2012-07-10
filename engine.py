import game_controller


class Engine:
    '''
    Class manages one game match.
    Usage:
        >> eng = Engine(game_master)
        >> eng.play()
    '''
    def __init__(self, GameMaster):
        '''
        Constructor of class Engine.
        Creates an object of the class, gets game master constructor
        '''
        self._GameMaster = GameMaster
        self._game_controller = game_controller.GameController()

    def play(self):
        '''
        Starts the game, executes master game program and gets log files,
        then finishes the game and kills all the bots
        '''
        game_master = self._GameMaster()
        self._game_controller.create_bots()
        while not self._game_controller.isfinished:
            game_master.tick(self._game_controller)
        self._game_controller.kill_bots()
        return self._game_controller
