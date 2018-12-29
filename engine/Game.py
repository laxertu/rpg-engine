import sys, pygame

from engine.GameHero import GameHero
from engine.GameEnemy import GameEnemy
from model.Hero import Hero
from model.Abilities import Abilities
from model.Scene import Scene

class Game:
    def __init__(self):
        self.width = 640
        self.height = 480

        self._init_scene()


    def _init_scene(self):
        self.scene = Scene()

        game_hero = GameHero(hero=Hero('Player 1', Abilities()))
        self.scene.setHeroes([game_hero])

        game_enemy = GameEnemy(Abilities())
        self.scene.setEnemies([game_enemy])

    def run(self):

        pygame.init()
        screen = pygame.display.set_mode([self.width, self.height])

        hero = pygame.image.load("./img/hero_default.png")
        hero_rect = hero.get_rect()
        hero_rect = hero_rect.move([0, 430])

        screen.fill([0, 0, 0])
        screen.blit(hero, hero_rect)
        pygame.display.flip()

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()




        
