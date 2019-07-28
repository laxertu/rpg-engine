from easyAI.TwoTeamsGame import TwoTeamsGame, AbstractOrderedPlayerSelector
from random import randint


class AbstractCharacter:

    def __init__(self, name: str):
        self.name = name

    def active(self) -> bool:
        raise NotImplementedError('Abstract method')

    def to_str(self):
        return ''


class Battle(TwoTeamsGame):
    def raw_teams(self):
        return self.player_selector.teams

    def setup_game(self):
        pass

    def show(self):
        pass

    def scoring(self):
        result = 0

        if self.is_over():
            return 1000000

        for p in self.current_opponent_team():
            result -= (p.pf_max() - p.pf()) + p.scoring()

        for p in self.current_team():
            result += p.pf() + p.scoring()

        return result

    def is_over(self):
        return len(self.current_team()) == 0 or len(self.current_opponent_team()) == 0

    def possible_moves(self):
        actor = self.current_player()
        result = []
        for target in [x for x in range(0, len(self.alive_enemies()))]:
            for action in actor.possible_moves(self):
                result.append(str(target) + '_' + action)
        return result

    def alive_enemies(self):
        return self.player_selector.opponent_team()

    def make_move(self, move: str):
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
            return action.do(source, dest)

        return 'FAILED'


class AdvPlayerSelector(AbstractOrderedPlayerSelector):

    def filter_team(self, team: list):
        ret = [e for e in team if e.active()]

        return ret

    def current_team_id(self) -> int:
        return self._current_team_id()

    def current_opposite_team_id(self):
        return (self.current_team_id() + 1) % 2

class BaseAction:
    _name = ''
    _probability = 0

    def probability(self):
        return self._probability

    def do(self, source: AbstractCharacter, dest: AbstractCharacter):
        raise NotImplementedError('Abstract method')

    def __str__(self):
        return self._name

    def to_str(self):
        return str(self)

    def simulate(self, source:AbstractCharacter, dest:AbstractCharacter) -> str:
        raise NotImplementedError('Abstract method')

    def get_name(self):
        return self._name

class NoneAction(BaseAction):
    def to_str(self):
        return ''

    def do(self, source: AbstractCharacter, dest: AbstractCharacter):
        pass

    def simulate(self, source: AbstractCharacter, dest: AbstractCharacter) -> str:
        return ''

