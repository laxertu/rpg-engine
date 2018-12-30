
class BaseAction:

    def __init__(self, game):
        self.game = game

    def probability(self):
        return 0

    def do(self):
        pass

class SwordAttack(BaseAction):

    def do(self):
        pass