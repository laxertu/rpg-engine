from easyAI.TwoTeamsGame import *
from core.Game import Game
from entities.characters import Hero

t1 = [Hero('1'), Hero('2')]
t2 = [Hero('3'), Hero('4')]

g = Game(t1, t2)
g.run()