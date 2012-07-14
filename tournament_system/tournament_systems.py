from tournament_system.tournament_system_each import TournamentSystemEach
from tournament_system.tournament_system_olympic import TournamentSystemOlympic

tournament_systems = {
    "olympic": TournamentSystemOlympic,
    "round-robin": TournamentSystemEach
}
