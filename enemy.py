from easyAI import AI_Player, Negamax

class Enemy(AI_Player):
    def __init__(self, name = 'Malo'):
        super().__init__(Negamax(3), name)

        self.level = 0
        self.pf = 10
        self.armour = 5
        self.magic_resistance = 2
        self.attack = 5
        self.magic = 8

    def ask_move(self, game):
        print(self.name + ' says: ', end='')
        #print(self.name + ' states: ', end='', flush=True)
        result = self.AI_algo(game)
        print(result)
        return result
