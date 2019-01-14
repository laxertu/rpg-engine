from easyAI import Negamax
from game import Game as g, characters as c
from game.Game import AdvPlayerSelector

t1 = [c.Knight('Percebal'), c.Wizard('Langostin'), c.Knight('Mejillon')]
t2 = [c.Daemon(Negamax(4), name='Sauron'), c.Troll(Negamax(4), 'Malvador'), c.EvilNun(Negamax(4), name='Madre Teresa de Calcuta')]

try:
    g = g.Game(t1, t2, AdvPlayerSelector)
    g.run()
except KeyboardInterrupt as e:
    print('Bye')