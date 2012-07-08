# -*- coding: utf-8 -*-

class TournamentSystem(self):
    def play_tournament():
        players=__load_players__()
        if self.tournament_type==1 :#на выбывание
            while len(players)>1:
                this_tour=Tour(players,tournament_type=1)
                players=this_tour.play()
                log.write(this_tour.log)
            