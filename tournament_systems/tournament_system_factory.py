import config
import tournament_systems_config as all_ts
#tournament_systems.


class TournamentSystemNotChoosedException(Exception):
    pass


class TournamentSystemNotFoundException(Exception):
    pass


def create():
    '''
    Get config and returns method
    that describes this type of game
    '''

    if not hasattr(config, 'tournament_system'):
        raise TournamentSystemNotChoosedException()
    if config.tournament_system in all_ts.tournament_systems:
        return all_ts.tournament_systems[config.tournament_system]
    else:
        raise TournamentSystemNotFoundException()
