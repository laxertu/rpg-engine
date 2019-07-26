from game.prefabs.fantasy_game.battle import Battle, AdvPlayerSelector
from game.prefabs.fantasy_game.characters import Character, BaseAction

class BattleWrapper:

    def __init__(self, team1, team2):
        self._battle = Battle(team1, team2, AdvPlayerSelector)
        self._t1_dict = dict()

        i = 0
        for t in team1:
            self._t1_dict[i] = t
            i += 1

        self._t2_dict = dict()

        i = 0
        for t in team2:
            self._t2_dict[i] = t
            i += 1


    def get_possible_moves(self):
        result = {}
        action_keys = self._battle.player.possible_moves(self._battle)

        for action_key in action_keys:
            result[action_key] = self._battle.player.abilities[action_key]

        return result

    def is_player_turn(self):
        return self._battle.player_selector.current_team_id() == 0

    def get_AI_selection(self) -> str:
        self._battle.switch_player()
        move = self._battle.player.ask_move(self._battle)
        return move

    def do_AI_move(self, move):
        result = self._make_move(move)
        self._battle.switch_player()
        return result

    def do_player_move(self, action_id: str, target_id: str):
        return self._make_move(self._build_player_move_str(action_id, target_id))

    def _build_player_move_str(self, action_id: str, target_id: str):

        """

        TwoTeamsGame gives arrays of teams without dead ones. here we perform a "map"
        TwoTeamsGame should return teams as dicts

        :param action_id:
        :param target_id:
        :return:
        """


        target = self._t2_dict[int(target_id)]
        i = 0
        for battle_target in self._battle.current_opponent_team():
            if battle_target is target:
                return str(i) + '_' + action_id
            i += 1


    def _make_move(self, move):
        result = self._battle.make_move(move)
        return result

    def get_move_txt(self, move):
        action, target = self._parse_move_str(move)
        return self._battle.player.name + ': ' + action.get_name() + ' -> ' + target.name

    def _parse_move_str(self, raw_selection: str) -> (BaseAction, Character):
        parsed_result = raw_selection.split('_')
        target_id = int(parsed_result[0])

        target = self._battle.current_opponent_team()[target_id]
        action = self._battle.player.abilities[parsed_result[1]]

        return action, target


    def game_over(self):
        return self._battle.is_over()

    def get_action_simuation_text(self, action_id: str, target_id: str):
        move = self._build_player_move_str(action_id, target_id)
        action, target = self._parse_move_str(move)

        return action.simulate(self._battle.current_player(), target)
