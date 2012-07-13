import config
from tournament_systems import tournament_systems


class NoSuchTournamentSystemException:
    pass


class TournamentSystemFactory:
    def run(config):
        if (config.tournament_system in tournament_systems):
            return tournament_systems[config.tournament_system]
        else:
            raise NoSuchTournamentSystemException(
                "There is no such tourtament system"
            )
