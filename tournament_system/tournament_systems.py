from tournament_system.tournament_system_each import TournamentSystemEach
from tournament_system import tournament_system_olympic

tournament_systems = {
    "olympic": tournament_system_olympic.TournamentSystemOlympic,
    "round-robin": TournamentSystemEach
}
