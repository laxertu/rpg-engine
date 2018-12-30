from random import randint

class Destruction:

    def probability(self, player):
        return 0.7

    def do(self, game):
        game.opponent.pf -= randint(1, 5) + game.player.attack
