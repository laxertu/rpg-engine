from easyAI.TwoTeamsGame import TwoTeamsGame, AbstractOrderedPlayerSelector

from random import randint
from game import render


class Game(TwoTeamsGame):

    def setup_game(self):
        self.renderer = render.UnixConsoleRederer()


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
        parsed_move = move.split('_')

        source = self.current_player()

        team = self.current_opponent_team()
        dest = team[int(parsed_move[0])]

        action = source.abilities[parsed_move[1]]


        #if randint(1, 100) <= action.probability() or self.ai_scoring_game:
        if randint(1, 100) <= action.probability():
            return action.do(self, source, dest)

        return ''


    def _do_action(self, action):
        if randint(1, 100) <= action.probability():
            action.do(self)

    def show(self):
        self.renderer.renderAskMove(self)

    def run(self):
        #os.system('clear')

        for self.nmove in range(5000):
            self.show()
            print(self.player.name + '\'s Turn', end='')
            move = self.player.ask_move(self)
            print('')
            parsed_result = move.split('_')

            target = self.current_opponent_team()[int(parsed_result[0])]
            attack = self.player.abilities[parsed_result[1]].name

            print(self.player.name + ' makes a ' + attack + ' to ' + target.name+' ')
            action_result = self.make_move(move)
            print(action_result + ' ', end='')
            input()


            if self.is_over():
                #os.system('clear')
                self.show()
                print('DESTRUCTION')
                print('')
                print('')
                break

            self.switch_player()
            #self.show()


class AdvPlayerSelector(AbstractOrderedPlayerSelector):

    def filter_team(self, team):
        ret = [e for e in team if e.pf() > 0]

        return ret