from random import randint

class AttackSword:

    def probability(self, game):
        return 70

    def do(self, game):
        game.opponent.pf -= randint(1, 5) + game.player.attack
