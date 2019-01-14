from game import actions as a
from easyAI import AI_Player
from game import Game

class Character:

    def __init__(self, name: str):
        self.name = name

        self._level = 0
        self._pf_max = 20
        self._pf = self._pf_max
        self._armour = 0
        self._magic_resistance = 0
        self._attack = 3
        self._magic = 3

        self._armour_penalty = 0
        self._magic_penalty = 0

        self.abilities = {}

    def __str__(self):
        result = ''
        result += self.name

        if self.pf() > 0:
            result += ' Hp: ' + str(self.pf())
        else:
            result += ' [DEAD]'


        result += "\n"
        result += ' Level: ' + str(self._level) + ' Arm: ' + str(self.armour()) + ' Res: ' + str(self.magic_resistance())
        if self._armour_penalty:
            result += ' [ARMOUR PENALTY]'

        if self._magic_penalty:
            result += ' [MAGIC PENALTY]'

        return result

    def pf(self):
        return max(0, self._pf)

    def pf_max(self):
        return self._pf_max

    def armour(self):
        return self._armour - self._armour_penalty

    def magic_resistance(self):
        return self._magic_resistance - self._magic_penalty

    def phisical_attack(self):
        return self._attack

    def phisical_resistence(self):
        """
        alias for self.armour
        :return:
        """
        return self.armour()

    def magic_attack(self):
        return self._magic

    def setActions(self, actions: dict):
        self.abilities = actions

    def doAction(self, action: str):
        self.abilities[action].do()

    def receivePhisicalDamage(self, amount: int):
        damage = max(0, amount - self.phisical_resistence())
        self._pf -= damage
        return self.name + ': -' + str(damage) + ' pf'

    def receiveMagicDamage(self, amount: int):
        damage = max(0, amount - self.magic_resistance())
        self._pf -= damage
        return self.name + ': -' + str(damage) + ' pf'

    def receiveArmourPenalty(self, amount: int):
        self._armour_penalty += amount
        return self.name + ': -' + str(amount) + ' armour'

    def receiveMagicPenalty(self, amount: int):
        self._magic_penalty += amount
        return self.name + ': -' + str(amount) + ' magic defense'

    def possibleMoves(self, game: Game):
        return self.abilities.keys()

    def scoring(self):
        return self.magic_resistance() + self.magic_attack() + self.phisical_resistence() + self.phisical_attack()

class HumanPlayer(Character):

    def ask_move(self, game: Game):
        return game.controller().action_selection_modal(game)


class Knight(HumanPlayer):

    def __init__(self, name: str):
        super().__init__(name)

        self._pf_max = 30
        self._pf = self._pf_max
        self._armour = 5
        self._magic_resistance = 0
        self._attack = 7
        self._magic = 0

        self.abilities = {'1': a.SwordAttack(), '2': a.Destruction()}


class Wizard(HumanPlayer):

    def __init__(self, name: str):
        super().__init__(name)

        self._pf_max = 15
        self._pf = self._pf_max
        self._armour = 0
        self._magic_resistance = 10
        self._attack = 0
        self._magic = 5

        self.abilities = {'1': a.MagicPenalty(), '2': a.FireBall()}

class AdvAI(AI_Player, Character):

    def __init__(self, AI_algo, name = 'AI'):
        AI_Player.__init__(self, AI_algo, name)
        Character.__init__(self, name)

    def possibleMoves(self, game: Game):
        return self.abilities.keys()

    def ask_move(self, game):
        result = self.AI_algo(game)
        return result


class Daemon(AdvAI):

    def __init__(self, AI_algo, name = 'Daemon'):
        AdvAI.__init__(self,AI_algo, name)
        self.abilities = {'1': a.ArmourPenalty(), '2': a.SwordAttack()}

class EvilNun(AdvAI):

    def __init__(self, AI_algo, name = 'Evil Nun'):
        AdvAI.__init__(self, AI_algo, name)
        self.abilities = {'1': a.MagicPenalty(), '2': a.FireBall()}

class Troll(AdvAI):

    def __init__(self, AI_algo, name = 'Troll'):
        AdvAI.__init__(self, AI_algo, name)
        self.abilities = {'1': a.ArmourPenalty(), '2': a.Destruction()}
