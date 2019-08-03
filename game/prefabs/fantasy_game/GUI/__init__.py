import os
from game.battle.GUI.graphics.pygame import core
from game.battle.GUI.graphics.pygame.component import ChrSprite

core.IMG_BASE_PATH = os.path.split(os.path.abspath(__file__))[0]+'/img/'

ChrSprite.icons = {
    'Knight': 'knight',
    'Wizard': 'wizard',
    'Daemon': 'sauron',
    'EvilNun': 'mt',
    'grave': 'grave',
}