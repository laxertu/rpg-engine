from game import characters
from game import Game

class BaseAction:
    name = ''

    def probability(self):
        return 0

    def do(self, source: characters, dest: characters):
        return ''

class SwordAttack(BaseAction):

    name = 'Sword attack'

    def probability(self):
        return 80

    def do(self, source, dest):
        return dest.receivePhisicalDamage(8 + source.phisical_attack())

class Destruction(BaseAction):
    name = 'Destruction'

    def probability(self):
        return 20

    def do(self, source: characters, dest: characters):
        return dest.receivePhisicalDamage(12 + source.phisical_attack())

class FireBall(BaseAction):

    name = 'Fire ball'

    def probability(self):
        return 50

    def do(self, source: characters, dest: characters):
        return dest.receiveMagicDamage(8 + source.magic_attack())

class MagicPenalty(BaseAction):

    name = 'Magic penalty'

    def probability(self):
        return 50

    def do(self, source: characters, dest: characters):
        return dest.receiveMagicPenalty(8 + source.magic_attack())



class ArmourPenalty:
    name = 'Armour penalty'

    def probability(self):
        return 20

    def do(self, source: characters, dest: characters):
        return dest.receiveArmourPenalty(3 + source.phisical_attack())
        pass
