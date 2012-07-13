import config
import tournament_systems as all_ts


class TournamentSystemNotFoundException(Exception):
    pass


class TournamentSystemFactory:
    '''
    Get config and returns method
    that describes this type of game
    '''
    def create(self):
        if config.tournament_system in all_ts.tournament_systems:
            return all_ts.tournament_systems[config.tournament_system]()
        else:
            raise TournamentSystemNotFoundException(
                "There is no such tourtament system"
            )
