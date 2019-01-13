from easyAI.TwoTeamsGame import TwoTeamsGame, AbstractOrderedPlayerSelector

from random import randint
from game import controller


class Game(TwoTeamsGame):

    def setup_game(self):
        self.controller = controller.UnixConsoleController()


    def scoring(self):
        result = 0

        for p in self.current_opponent_team():
            result -= p.pf() - p.pf_max() + p.scoring()

        for p in self.current_team():
            result -= p.pf() - p.pf_max() + p.scoring()

        return result

    def is_over(self):
        return len(self.current_team()) == 0 or len(self.current_opponent_team()) == 0


    def possible_moves(self):
        actor = self.current_player()
        result = []
        for target in [x for x in range(0, len(self.alive_enemies()))]:
            for action in actor.possibleMoves(self):
                result.append(str(target) + '_' + action)
        return result

    def alive_enemies(self):
        return self.player_selector.opponent_team()


    def make_move(self, move):
        """
        This method for compatibility with easyAI
        :param move:
        :return:
        """
        parsed_move = move.split('_')

        source = self.current_player()

        team = self.current_opponent_team()
        dest = team[int(parsed_move[0])]

        action = source.abilities[parsed_move[1]]
        if randint(1, 100) <= action.probability():
            return action.do(self, source, dest)

        return ''

    def run(self):

        for self.nmove in range(5000):
            self.controller.next_move(self)

            if self.is_over():
                self.controller.game_over()
                break

            self.switch_player()


class AdvPlayerSelector(AbstractOrderedPlayerSelector):

    def filter_team(self, team):
        ret = [e for e in team if e.pf() > 0]

        return ret