import pygame, sys

import game as g
import hero as h
import enemy as e

x = g.game([h.Hero('Percibel'), e.Enemy('Langostin')])
x.run()