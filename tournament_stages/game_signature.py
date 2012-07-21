class GameSignature:

    round_name = None

    def __init__(self, tournament_id=None, round_id=None, series_id=None,
                 game_id=None):
        self.round_id = round_id
        self.series_id = series_id
        self.game_id = game_id
        self.tournament_id = tournament_id

    def __lt__(self, signature):
        self_tuple = (self.tournament_id, self.round_id,
                      self.series_id, self.game_id)
        signature_tuple = (signature.tournament_id, signature.round_id,
                           signature.series_id, signature.game_id)
        return self_tuple < signature_tuple

    def __repr__(self):
        if self.round_name is None:
            return '<GameSignature ({}, {}, {}, {})>'.format(
                self.tournament_id, self.round_id,
                self.series_id, self.game_id)
        else:
            return '<GameSignature ({}, {} ({}), {}, {})>'.format(
                self.tournament_id, self.round_id,
                self.round_name, self.series_id, self.game_id)
