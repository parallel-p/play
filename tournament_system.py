# -*- coding: utf-8 -*-

class TournamentSystem():
    def play_tournament(self):
        players=__load_players__()
        if self.tournament_type==1 :#knockout
            while len(players)>1:
                this_tour=Tour(players,tournament_type=1)
                players=this_tour.play()
                log.write(this_tour.log)
            