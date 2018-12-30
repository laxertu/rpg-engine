from easyAI import Human_Player, AI_Player, Negamax, TwoPlayersGame
import destruction, move_attack_sword
from random import randint

class game(TwoPlayersGame):

    def __init__(self, players):
        self.players = players
        self.nplayer = 1
        self.num_rounds = 0

    def scoring(self):
        if self.is_over():
            return 1000

        result = -self.opponent.pf

        return result

    def possible_moves(self):
        result = ['sword', 'destruction']
        return result

    def make_move(self, move):
        if move == 'sword':
            action = move_attack_sword.AttackSword()
            self._do_action(action)

        if move == 'destruction':
            action = destruction.Destruction()
            self._do_action(action)

    def _do_action(self, action):
        if randint(1, 100) <= action.probability(self):
            action.do(self)


    def is_over(self):
        return self.player.pf <= 0 or self.opponent.pf <= 0

    def show(self):
        print('*****************')
        print(self.player.name + ' ' + str(self.player.pf))
        print(self.opponent.name + ' ' + str(self.opponent.pf))
        print('*****************')



    def run(self):
        self.show()
        for self.nmove in range(5000):

            move = self.player.ask_move(self)
            self.make_move(move)
            self.switch_player()
            self.show()

            if self.is_over():
                print('And the winner is:' + self.player.name)
                break
