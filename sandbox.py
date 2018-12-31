from easyAI.TwoTeamsGame import *
from core.Game import Game
from entities.characters import Hero, AdvAI
from easyAI import Negamax


t1 = [Hero('Percebal'), Hero('Langostin')]
t2 = [AdvAI(Negamax(4), name='Sauron'), AdvAI(Negamax(4), name='Madre Teresa de Calcuta')]

try:
    g = Game(t1, t2)
    g.run()
except KeyboardInterrupt as e:
    print('Bye')