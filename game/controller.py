import os

from game import Game

class BaseController:

    def next_move(self, game: Game):
        raise NotImplementedError('Abstract method')

    def game_over(self, game: Game):
        raise NotImplementedError('Abstract method')

    def action_selection_modal(self, game: Game):
        raise NotImplementedError('Abstract method')

    def _parse_raw_selection(self, game, raw_selection):
        parsed_result = raw_selection.split('_')

        target = game.current_opponent_team()[int(parsed_result[0])]
        attack = game.player.abilities[parsed_result[1]].name

        return attack, target

    def _do_player_selection(self, game):
        raw_selection = game.player.ask_move(game)
        attack, target = self._parse_raw_selection(game, raw_selection)
        action_result = game.make_move(raw_selection)

        return attack, target, action_result


class UnixConsoleController(BaseController):

    def next_move(self, game: Game):
        self._print_resume(game)
        print(game.player.name + '\'s Turn')

        attack, target, action_result = self._do_player_selection(game)

        print(game.player.name + ' makes a ' + attack + ' to ' + target.name + ' ')
        print('')
        print('***** ' + action_result + ' *****')
        print('')
        print('Press [ENTER] to continue > ', end='')
        input()

    def game_over(self, game: Game):
        self._print_resume(game)
        print('**DESTRUCTION**')
        print('')

    def action_selection_modal(self, game: Game):

        player_abilities = game.player.abilities

        actions_available = player_abilities.keys()
        enemies_available = game.alive_enemies()

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
                print(' ' + ak + ': ' + player_abilities[ak].name)

            print('')
            print('Action: ', end='')
            move = input()

        return str(target_id - 1) + '_' + move


    def _print_resume(self, game: Game):
        os.system('clear')
        print('*****************')
        for hero in game.player_selector.teams[0]:
            if hero.pf() <= 0:
                print('[DEAD] ', end='')
            print(hero)

        print('')
        for enemy in game.player_selector.teams[1]:
            if enemy.pf() <= 0:
                print('[DEAD] ', end='')
            print(enemy)

        print('*****************')
        print('')