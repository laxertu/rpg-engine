#from entities.characters import Character


class BaseAction:
    name = ''

    def probability(self):
        return 0

    def do(self, game, source, dest):
        pass

class SwordAttack(BaseAction):

    name = 'Sword attack'

    def probability(self):
        return 80

    def do(self, game, source, dest):
        dest.receivePhisicalDamage(8)
        pass

class Destruction(BaseAction):
    name = 'Destruction'

    def probability(self):
        return 20

    def do(self, game, source, dest):
        dest.receivePhisicalDamage(12)
        pass
