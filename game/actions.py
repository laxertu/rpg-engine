from game import characters
from game import Game

class BaseAction:
    name = ''

    def probability(self):
        return 0

    def do(self, game: Game, source: characters, dest: characters):
        return ''

class SwordAttack(BaseAction):

    name = 'Sword attack'

    def probability(self):
        return 80

    def do(self, game: Game, source: characters, dest: characters):
        return dest.receivePhisicalDamage(8)
        pass

class Destruction(BaseAction):
    name = 'Destruction'

    def probability(self):
        return 20

    def do(self, game: Game, source: characters, dest: characters):
        return dest.receivePhisicalDamage(12)

class ArmourPenalty:
    name = 'Armour penalty'

    def probability(self):
        return 20

    def do(self, game: Game, source: characters, dest: characters):
        return dest.receiveArmourPenalty(3)
        pass
