from core.Game import Game
from entities.actions import *

class Character:

    def __init__(self):
        self.level = 0
        self.pf = 12
        self.armour = 7
        self.magic_resistance = 2
        self.attack = 3
        self.magic = 0

        self.actions = {}

    def setActions(self, actions):
        self.actions = actions

    def doAction(self, action):
        self.actions[action].do()

    def possibleMoves(self, game: Game):
        return self.actions.keys()

class Hero(Character):

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.actions = {'1': SwordAttack(), '2': Destruction()}

    def ask_move(self, game: Game):

        actions_available = self.actions.keys()
        enemies_available = game.alive_enemies()

        target_ids = [x for x in range(1, len(enemies_available) + 1)]

        target_id = None
        while target_id not in target_ids:
            print('')
            enemy_id = 1
            for enemy in enemies_available:
                print(' ' + str(enemy_id) + ': ' + enemy.name)
                enemy_id += 1
            print('')
            print('Target: ', end = '')

            inputz = input()
            print('')
            if inputz:
                target_id = int(inputz)

        move = None
        while str(move) not in actions_available:

            for ak in sorted(self.actions.keys()):
                print(' ' + ak + ': ' + self.actions[ak].name)

            print('')
            print('Action: ', end='')
            move = input()

        return str(target_id - 1) + '_' + move


