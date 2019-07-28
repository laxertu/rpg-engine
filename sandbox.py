import pygame

import game.prefabs.fantasy_game.characters as c
from easyAI import Negamax

# SETUP

from game.prefabs.fantasy_game.manager import Manager



# TEAMS
t1 = [c.Knight('Percebal'), c.Wizard('Langostin')]
#t2 = [c.Knight('Percebal2'), c.Wizard('Langostin2')]

#t1 = [c.EvilNun(Negamax(4), name="MT"), c.Daemon(Negamax(4), name='Sauron')]
t2 = [c.EvilNun(Negamax(4), name="Madre Teresa de Calcuta"), c.Daemon(Negamax(4), name='Sauron')]


class BattleGui:
    def __init__(self):
        self._change_manager = None

    def show(self, team1, team2):

        self._change_manager = Manager(team1, team2)
        #self._change_manager.init_scene()

        while self._change_manager.next():
            pass

        pygame.quit()
        exit(0)

b = BattleGui()
b.show(t1, t2)



