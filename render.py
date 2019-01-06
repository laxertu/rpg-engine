import os


class UnixConsoleRederer:

    def renderAskMove(self, game):
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
