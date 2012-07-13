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

    def get_move(self, player, p_state, deserializer):
        '''
        Gets move to Bot instance
        '''
        player.get_move(p_state, move, deserializer)

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

    def get_players(self):
        '''
        Get's players list as an list of instances
        '''
        return self._players

    def create_bots(self):
        '''
        Creates ALL bots
        '''
        for player in self._players:
            player.create_process()

    def kill_bots(self):
        '''
        Killes ALL running bots
        '''
        for player in self._players:
            if player._is_running == True:
                player.kill_process()
