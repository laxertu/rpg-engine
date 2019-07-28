from game.battle.battle import Battle
from game.battle.battle import AdvPlayerSelector


class BaseBattleController:

    def __init__(self, team1, team2):
        self._battle = Battle(team1, team2, AdvPlayerSelector)

    def get_battle(self):
        return self._battle

    def next_move(self):
        raise NotImplementedError('Abstract method')

    def do_player_move(self, move: str):

        attack, target = self._parse_raw_selection(move)
        action_result = self._battle.make_move(move)

        return attack, target, action_result

    def do_enemy_move(self):
        if not self._battle.is_over():
            attack, target, action_result = self.next_move()
            return attack, target, action_result
        return None

    def next_player(self):

        cp = self._battle.current_player()
        cp.is_current_player = False
        self._battle.switch_player()
        cp = self._battle.current_player()
        cp.is_current_player = True

    def game_over(self):
        raise NotImplementedError('Abstract method')

    def action_selection_modal(self):
        raise NotImplementedError('Abstract method')

    def _parse_raw_selection(self, raw_selection: str):
        parsed_result = raw_selection.split('_')
        target_id = int(parsed_result[0])


        target = self._battle.current_opponent_team()[target_id]
        attack = self._battle.player.abilities[parsed_result[1]].name

        return attack, target

    def _do_player_selection(self, game: Battle):
        raw_selection = game.player.ask_move(game)

        if not raw_selection is None:
            attack, target = self._parse_raw_selection(raw_selection)
            action_result = game.make_move(raw_selection)

            return attack, target, action_result
        return None, None, None

    def print_resume(self):
        import os
        os.system('clear')
        print('*****************')
        print('* GOOD GUYS *')
        for hero in self._battle.player_selector.teams[0]:
            print(hero)
            print('')

        print('')
        print('* BAD GUYS *')
        for enemy in self._battle.player_selector.teams[1]:
            print(enemy)
            print('')

        print('*****************')
        self.print_turn()

    def get_resume_team_texts(self, team_id):
        result = []
        for hero in self._battle.player_selector.teams[team_id]:
            result.append(hero.__str__())

        return result

    def get_action_result_texts(self, attack, target, action_result):
        result = list()

        result.append(self._battle.player.name + ' makes a ' + attack + ' to ' + target.name)
        result.append('')
        result.append('***** ' + action_result + ' *****')

        return result

    def print_turn(self):
        print('')
        print(self._battle.player.name + '\'s Turn')

    def _print_action_result(self, attack, target, action_result):
        print(self._battle.player.name + ' makes a ' + attack + ' to ' + target.name + ' ')
        print('')
        print('***** ' + action_result + ' *****')


class PyGameBattleGUIController(BaseBattleController):

    def next_move(self):
        attack, target, action_result = self._do_player_selection(self._battle)

        return attack, target, action_result

    def game_over(self):
        return self.get_battle().is_over()

    def action_selection_modal(self):
        pass


class UnixConsoleController(BaseBattleController):

    def next_move(self):
        self.print_resume()

        attack, target, action_result = self._do_player_selection(self._battle)

        print(self._battle.player.name + ' makes a ' + attack + ' to ' + target.name + ' ')
        print('')
        print('***** ' + action_result + ' *****')
        print('')
        print('Press [ENTER] to continue > ', end='')
        input()

    def game_over(self):
        pass

    def action_selection_modal(self):

        player_abilities = self._battle.player.abilities

        actions_available = player_abilities.keys()
        enemies_available = self._battle.alive_enemies()

        target_ids = [x for x in range(1, len(enemies_available) + 1)]

        target_id = None
        while target_id not in target_ids:
            print('')
            enemy_id = 1
            for enemy in enemies_available:
                print(' ' + str(enemy_id) + ': ' + enemy.name)
                enemy_id += 1
            print('')
            print('Target: ', end = '')

            inputz = input()
            print('')
            if inputz:
                target_id = int(inputz)

        move = None
        while str(move) not in actions_available:

            for ak in sorted(player_abilities.keys()):
                print(' ' + ak + ': ' + player_abilities[ak].name + ' ' +  str(player_abilities[ak].probability()) + '%')

            print('')
            print('Action: ', end='')
            move = input()

        return str(target_id - 1) + '_' + move

