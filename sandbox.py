from easyAI.TwoTeamsGame import *
from core.Game import Game
from entities.characters import Hero

t1 = [Hero('Percebal'), Hero('Langostin')]
t2 = [Hero('Malo 1'), Hero('Malo 2')]

g = Game(t1, t2)
g.run()