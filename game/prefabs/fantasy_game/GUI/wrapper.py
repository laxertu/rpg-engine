from game.prefabs.fantasy_game.battle import Battle, AdvPlayerSelector
from game.prefabs.fantasy_game.characters import Character, BaseAction

class BattleWrapper:

    def __init__(self, team1, team2):
        self._battle = Battle(team1, team2, AdvPlayerSelector)

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
        move = target_id+'_'+action_id
        return self._make_move(move)

    def _make_move(self, move):
        result = self._battle.make_move(move)
        #print(result)
        return result

    def get_move_txt(self, move):
        action, target = self._parse_move_str(move)
        return self._battle.player.name + ': ' + action.name + ' -> ' + target.name

    def _parse_move_str(self, raw_selection: str) -> (BaseAction, Character):
        parsed_result = raw_selection.split('_')
        target_id = int(parsed_result[0])


        target = self._battle.current_opponent_team()[target_id]
        action = self._battle.player.abilities[parsed_result[1]]

        return action, target


    def game_over(self):
        return self._battle.is_over()
