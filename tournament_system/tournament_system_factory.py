import config
from tournament_systems import tournament_systems


class TournamentSystemNotFoundException:
    pass


class TournamentSystemFactory:
    '''
    Get config and returns method
    that describes this type of game
    '''
    def create(self):
        if config.tournament_system in tournament_systems:
            return tournament_systems[config.tournament_system]()
        else:
            raise TournamentSystemNotFoundException(
                "There is no such tourtament system"
            )
