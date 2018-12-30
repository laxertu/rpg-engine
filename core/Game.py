from easyAI.TwoTeamsGame import TwoTeamsGame
from easyAI.TwoTeamsGame import OrderedPlayerSelector
from entities.actions import SwordAttack
from random import randint

class Game(TwoTeamsGame):

    def __init__(self, team1, team2):
        self.player_selector = OrderedPlayerSelector(team1, team2)
        self.nplayer = 1

    def scoring(self):
        result = 1000
        return result

    def possible_moves(self):
        result = ['sword', 'destruction']
        return result

    def make_move(self, move):
        if move == 'sword':
            action = SwordAttack(game=self)
            self._do_action(action)

    def _do_action(self, action):
        if randint(1, 100) <= action.probability():
            action.do(self)


    def is_over(self):
        pfs = 0
        for enemy in self.current_opponent_team():
            pfs += enemy.pf

        return pfs <= 0

    def show(self):
        print('*****************')
        for hero in self.player_selector.current_team():
            print(hero.name + ' ' + str(hero.pf))
        print('*****************')

        for enemy in self.player_selector.opponent_team():
            print(enemy.name + ' ' + str(enemy.pf))

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
