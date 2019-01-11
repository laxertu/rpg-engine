from game import actions as a
from easyAI import AI_Player
from game import Game

class Character:

    def __init__(self):
        self._level = 0
        self._pf = 12
        self._armour = 7
        self._magic_resistance = 2
        self._attack = 3
        self._magic = 0

        self._armour_penalty = 0

        self.abilities = {}

    def __str__(self):
        result = ''
        result += self.name
        result += ' Pf: ' + str(self.pf())
        #result += "\n"
        #result += ' level ' + str(self._level) + ' Arm: ' + str(self.armour()) + ' Res: ' + str(self.magic_resistance())
        if self._armour_penalty:
            result += ' ARMOUR PENALTY'

        return result

    def pf(self):
        return self._pf

    def armour(self):
        return self._armour - self._armour_penalty

    def magic_resistance(self):
        return self._magic_resistance

    def phisical_attack(self):
        return self._attack

    def magic_attack(self):
        return self._magic

    def setActions(self, actions: dict):
        self.abilities = actions

    def doAction(self, action: str):
        self.abilities[action].do()

    def receivePhisicalDamage(self, amount: int):
        #self._pf -= max(0, self.armour() - amount)
        self._pf -= amount
        return self.name + ': -' + str(amount) + ' pf'

    def receiveMagicDamage(self, amount: int):
        damage = max(0, self.magic_resistance() - amount)
        self._pf -= damage
        return self.name + ': -' + damage + ' pf'

    def receiveArmourPenalty(self, amount: int):
        self._armour_penalty += amount
        return self.name + ': -' + str(amount) + ' armour'

    def possibleMoves(self, game: Game):
        return self.abilities.keys()

class HumanPlayer(Character):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def ask_move(self, game: Game):

        actions_available = self.abilities.keys()
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

            for ak in sorted(self.abilities.keys()):
                print(' ' + ak + ': ' + self.abilities[ak].name)

            print('')
            print('Action: ', end='')
            move = input()

        return str(target_id - 1) + '_' + move

class Knight(HumanPlayer):

    def __init__(self, name: str):
        super().__init__(name)
        self.abilities = {'1': a.SwordAttack(), '2': a.Destruction()}


#ArmourPenalty

class AdvAI(AI_Player, Character):

    def __init__(self, AI_algo, name = 'AI'):
        AI_Player.__init__(self, AI_algo, name)
        Character.__init__(self)
        self.abilities = {'1': a.SwordAttack(), '2': a.Destruction()}

    @property
    def actions(self):
        return {'1': a.SwordAttack(), '2': a.Destruction()}

    def possibleMoves(self, game):
        return self.abilities.keys()

    def ask_move(self, game):
        result = self.AI_algo(game)
        return result


class Demon(AdvAI):
    def __init__(self, AI_algo, name = 'AI'):
        AdvAI.__init__(self,AI_algo, name)
        self.abilities = {'1': a.ArmourPenalty(), '2': a.Destruction()}
