from random import randint

from copy import deepcopy
from game import render


class TwoTeamsGame:

    def play(self, nmoves=1000, verbose=True):

        history = []

        if verbose:
            self.show()

        for self.nmove in range(1, nmoves + 1):

            if self.is_over():
                break

            move = self.player.ask_move(self)
            history.append((deepcopy(self), move))
            self.make_move(move)

            if verbose:
                self.show()

            self.switch_player()

        history.append(deepcopy(self))

        return history

    #@property
    #def nopponent(self):
     #   return 2 if (self.nplayer == 1) else 1


    @property
    def opponent_team(self):
       return self.current_opponent_team()

    @property
    def player(self):
        return self.current_player()

    def current_player(self):
        return self.player_selector.current_player()

    def current_opponent_team(self):
        return self.player_selector.opponent_team()

    def current_team(self):
        return self.player_selector.current_team()

    def switch_player(self):
        self.player_selector.next_player()

    def copy(self):
        return deepcopy(self)

    def get_move(self):
        """
        Method for getting a move from the current player. If the player is an
        AI_Player, then this method will invoke the AI algorithm to choose the
        move. If the player is a Human_Player, then the interaction with the
        human is via the text terminal.
        """
        return self.player.ask_move(self)

    def play_move(self, move):
        """
        Method for playing one move with the current player. After making the move,
        the current player will change to the next player.

        Parameters
        -----------

        move:
          The move to be played. ``move`` should match an entry in the ``.possibles_moves()`` list.
        """
        result = self.make_move(move)
        self.switch_player()
        return result

class OrderedPlayerSelector:

    def __init__(self, team1, team2):
        self.teams = [team1, team2]
        self.move_no = 0
        self.counters = [0, 0]

    def filter_team(self, team):
        return team

    def current_player(self):

        team_id = self._current_team_id()
        team = self.current_team()

        character_id = self.counters[team_id] % len(team)

        return team[character_id]

    def _current_team_id(self):
        return self.move_no % 2

    def _next_team_id(self):
        return (self.move_no + 1) % 2

    def next_player(self):
        team_id = self._current_team_id()
        self.counters[team_id] += 1
        self.move_no += 1

    def current_team(self):
        return self.filter_team(self.teams[self._current_team_id()])

    def opponent_team(self):
        return self.filter_team(self.teams[self._next_team_id()])

class Game(TwoTeamsGame):

    def __init__(self, team1, team2):
        self.player_selector = AdvPlayerSelector(team1, team2)
        self.nplayer = 1
        self.move_output = ''
        self.renderer = render.UnixConsoleRederer()

    def scoring(self):
        result = 1000
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

        #print(source.name + ' makes an ' + action.name +' to ' + dest.name)
        return action.do(self, source, dest)
        #os.system('clear')


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


class AdvPlayerSelector(OrderedPlayerSelector):


    def filter_team(self, team):

        #print("Before: " + str(team))
        ret = [e for e in team if e.pf() > 0]
        #print("After: " + str(ret))

        return ret