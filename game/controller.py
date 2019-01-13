import os

from game import Game

class BaseController:

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
        print(action_result + ' ', end='')
        print('[ENTER] to continue')
        input()


    def _print_resume(self, game: Game):
        os.system('clear')
        print('*****************')
        for hero in game.player_selector.teams[0]:
            if hero.pf() <= 0:
                print('[DEAD]', end='')
            print(hero)

        print('')
        for enemy in game.player_selector.teams[1]:
            if enemy.pf() <= 0:
                print('[DEAD]', end='')
            print(enemy)

        print('*****************')
        print('')

    def game_over(self):
        self._print_resume()
        print('DESTRUCTION')
        print('')
        print('')
