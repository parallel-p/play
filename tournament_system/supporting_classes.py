class GameSignature:

    def __init__(self, tournament_id=None, round_id=None, series_id=None,
                 game_id=None):
        self.round_id = round_id
        self.series_id = series_id
        self.game_id = game_id
        self.tournament_id = tournament_id
