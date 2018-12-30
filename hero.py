class Hero:
    def __init__(self, name = 'Ser Organico'):
        self.name = name

        self.level = 0
        self.pf = 12
        self.armour = 7
        self.magic_resistance = 2
        self.attack = 3
        self.magic = 0


    def ask_move(self, game):
        possible_moves_str = list(map(str, game.possible_moves()))
        move = None
        while str(self.mapkey(move)) not in possible_moves_str:
            print(self.name + ' says: ', end='')
            move = input()
            print(self.mapkey(move))
        return self.mapkey(move)

    def mapkey(self, key):
        if key == '1':
            return 'sword'

        if key == '2':
            return 'destruction'

        return ''

class AttackSword():

    def do(self, game):
        game.opponent.pf -= 20 - game.opponent.armour



