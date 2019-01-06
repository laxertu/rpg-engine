import characters as c
from easyAI import Negamax
import Game as g

t1 = [c.Knight('Percebal'), c.Knight('Langostin')]
t2 = [c.Demon(Negamax(4), name='Sauron'), c.AdvAI(Negamax(4), name='Madre Teresa de Calcuta')]

try:
    g = g.Game(t1, t2)
    g.run()
except KeyboardInterrupt as e:
    print('Bye')