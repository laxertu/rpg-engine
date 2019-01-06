import characters as c
import Game as g

class BaseAction:
    name = ''

    def probability(self):
        return 0

    def do(self, game: g.Game, source, dest):
        return ''

class SwordAttack(BaseAction):

    name = 'Sword attack'

    def probability(self):
        return 80

    def do(self, game, source, dest):
        return dest.receivePhisicalDamage(8)
        pass

class Destruction(BaseAction):
    name = 'Destruction'

    def probability(self):
        return 20

    def do(self, game, source, dest):
        return dest.receivePhisicalDamage(12)

class ArmourPenalty:
    name = 'Armour penalty'

    def probability(self):
        return 20

    def do(self, game, source, dest):
        return dest.receiveArmourPenalty(3)
        pass
