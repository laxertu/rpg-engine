from easyAI.TwoTeamsGame import TwoTeamsGame
from easyAI.TwoTeamsGame import OrderedPlayerSelector
from entities.actions import SwordAttack
from random import randint

import os

class Game(TwoTeamsGame):

    def __init__(self, team1, team2):
        self.player_selector = AdvPlayerSelector(team1, team2)
        self.nplayer = 1

    def scoring(self):
        result = 1000
        return result

    def is_over(self):
        return len(self.current_team()) == 0 or len(self.current_opponent_team()) == 0


    def possible_moves(self, actor):

        result = []
        for target in self.alive_enemies():
            for action in actor.possibleMoves(self):
                result.append(str(target) + '_' + action)
        return result

    def alive_enemies(self):
        return self.player_selector.opponent_team()


    def make_move(self, move):
        parsed_move = move.split('_')

        source = self.current_player()

        team = self.current_opponent_team()
        dest = team[int(parsed_move[0])]

        action = source.actions[parsed_move[1]]

        print(source.name + ' makes an ' + action.name +' to ' + dest.name)
        action.do(self, source, dest)

        os.system('clear')


    def _do_action(self, action):
        if randint(1, 100) <= action.probability():
            action.do(self)

    def show(self):
        print('*****************')
        for hero in self.player_selector.teams[0]:
            if hero.pf <= 0:
                print('[DEAD]', end='')
            print(hero.name + ' ' + str(hero.pf))

        print('')
        for enemy in self.player_selector.teams[1]:
            if enemy.pf <= 0:
                print('[DEAD]', end='')
            print(enemy.name + ' ' + str(enemy.pf))

        print('*****************')
        print('')


    def run(self):
        os.system('clear')

        self.show()
        for self.nmove in range(5000):
            print(self.player.name + '\'s Turn')
            move = self.player.ask_move(self)
            self.make_move(move)

            if self.is_over():
                print('And the winner is:' + self.player.name)
                print('')
                print('')
                break

            self.switch_player()
            self.show()


class AdvPlayerSelector(OrderedPlayerSelector):


    def filter_team(self, team):

        #print("Before: " + str(team))
        ret = [e for e in team if e.pf > 0]
        #print("After: " + str(ret))

        return ret