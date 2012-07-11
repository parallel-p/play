class GameSignature:

    def __init__(self, tournament_id=None, round_id=None, series_id=None,
                 game_id=None):
        self.round_id = round_id
        self.series_id = series_id
        self.game_id = game_id
        self.tournament_id = tournament_id

    def __lt__(self, signature):
        if self.tournament_id == signature.tournament_id:
            if self.series_id == signature.series_id:
                if self.game_id == signature.game_id:
                    return False
                else:
                    return self.game_id < signature.game_id
            else:
                return self.series_id < signature.series_id
        else:
            return self.tournament_id < signature.tournament_id
