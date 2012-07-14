from tournament_system import tournament_system_each
from tournament_system import tournament_system_olympic

tournament_systems = {
    "olympic": tournament_system_olympic.TournamentSystemOlympic,
    "round-robin": tournament_system_each.TournamentSystemEach
}
