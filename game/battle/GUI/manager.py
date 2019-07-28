from game.battle.GUI.mediator import WindowManager

import os

class UnixConsoleWM(WindowManager):
    def init_scene(self):
        print('Welcome to BATTLE')

    def erase_screen(self):
        os.system('clear')

    def display_all(self):
        pass

    def display_endgame(self):
        print('END GAME')

class AbstractBattleManager:
    def __init__(self, team1, team2):
        pass