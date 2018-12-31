import os, sys

basedir = os.path.dirname(os.path.abspath(__file__))
print(basedir + '/core')
sys.path.append(basedir + '/core')
sys.path.append(basedir + '/entities')

from core.Game import Game
from entities.characters import *
from easyAI import Negamax

t1 = [Knight('Percebal'), Knight('Langostin')]
t2 = [Demon(Negamax(4), name='Sauron'), AdvAI(Negamax(4), name='Madre Teresa de Calcuta')]

try:
    g = Game(t1, t2)
    g.run()
except KeyboardInterrupt as e:
    print('Bye')