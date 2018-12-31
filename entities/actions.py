
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
        dest.pf -= 5
        pass

class Destruction(BaseAction):
    name = 'Destruction'

    def probability(self):
        return 20

    def do(self, game, source, dest):
        dest.pf -= 10
        pass
