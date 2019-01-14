from easyAI import Negamax
from game.prefabs.fantasy_game import characters as c, battle as g
from game.prefabs.fantasy_game.battle import AdvPlayerSelector

t1 = [c.Knight('Percebal'), c.Wizard('Langostin'), c.Knight('Mejillon')]
t2 = [c.Daemon(Negamax(4), name='Sauron'), c.Troll(Negamax(4), 'Malvador'), c.EvilNun(Negamax(4), name='Madre Teresa de Calcuta')]

try:
    g = g.Battle(t1, t2, AdvPlayerSelector)
    g.run()
except KeyboardInterrupt as e:
    print('Bye')