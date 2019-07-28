from game.battle.battle import BaseAction, AbstractCharacter, Battle
from easyAI import AI_Player

class Character(AbstractCharacter):

    def __init__(self, name: str):

        super().__init__(name)

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
        self.is_current_player = False

    def __str__(self):
        result = ''
        result += self.name + "\n" + ' HP ' + str(self.pf()) + '/' + str(self.pf_max())
        return result

    def to_str(self):
        return str(self)

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

    def set_actions(self, actions: dict):
        self.abilities = actions

    def do_action(self, action: str):
        self.abilities[action].do()

    def receive_phisical_damage(self, amount: int):
        damage = max(0, amount - self.phisical_resistence())
        self._pf -= damage
        return self.name + ': -' + str(damage) + ' pf'

    def receive_magic_damage(self, amount: int):
        damage = max(0, amount - self.magic_resistance())
        self._pf -= damage
        return self.name + ': -' + str(damage) + ' pf'

    def receive_armour_penalty(self, amount: int):
        self._armour_penalty += amount
        return self.name + ': -' + str(amount) + ' armour'

    def receive_magic_penalty(self, amount: int):
        self._magic_penalty += amount
        return self.name + ': -' + str(amount) + ' magic defense'

    def possible_moves(self, battle: Battle):
        return self.abilities.keys()

    def scoring(self):
        return self.magic_resistance() + self.magic_attack() + self.phisical_resistence() + self.phisical_attack()

    def active(self) -> bool:
        return self.pf() > 0

class HumanPlayer(Character):
    pass





class Knight(HumanPlayer):

    def __init__(self, name: str):
        super().__init__(name)

        self._pf_max = 30
        self._pf = self._pf_max
        self._armour = 5
        self._magic_resistance = 0
        self._attack = 7
        self._magic = 0

        self.abilities = {'1': SwordAttack(), '2': Destruction()}



class Wizard(HumanPlayer):

    def __init__(self, name: str):
        super().__init__(name)

        self._pf_max = 15
        self._pf = self._pf_max
        self._armour = 0
        self._magic_resistance = 10
        self._attack = 0
        self._magic = 5

        self.abilities = {'1': MagicPenalty(), '2': FireBall()}


class AdvAI(AI_Player, Character):

    def __init__(self, AI_algo, name = 'AI'):
        AI_Player.__init__(self, AI_algo, name)
        Character.__init__(self, name)

    def ask_move(self, game):
        result = self.AI_algo(game)
        return result


class Daemon(AdvAI):

    def __init__(self, AI_algo, name = 'Daemon'):
        AdvAI.__init__(self,AI_algo, name)

        self._pf_max = 10
        self._pf = self._pf_max
        self._armour = 6
        self._magic_resistance = 12
        self._attack = 0
        self._magic = 3

        self.abilities = {'1': FireBall(), '2': ArmourPenalty()}


class EvilNun(AdvAI):

    def __init__(self, AI_algo, name = 'Evil Nun'):
        AdvAI.__init__(self, AI_algo, name)
        self._pf_max = 15
        self._pf = self._pf_max
        self._armour = 0
        self._magic_resistance = 10
        self._attack = 0
        self._magic = 5

        self.abilities = {'1': MagicPenalty(), '2': FireBall()}


class Troll(AdvAI):

    def __init__(self, AI_algo, name = 'Troll'):
        AdvAI.__init__(self, AI_algo, name)

        self._pf_max = 20
        self._pf = self._pf_max
        self._armour = 2
        self._magic_resistance = 0
        self._attack = 7
        self._magic = 0

        self.abilities = {'1': ArmourPenalty(), '2': Destruction()}

class Action(BaseAction):

    def do(self, source: AbstractCharacter, dest: AbstractCharacter):
        pass

    def simulate(self, source: AbstractCharacter, dest: AbstractCharacter) -> str:
        pass


class BasePhisicalAttack(Action):

    _name = ''
    _base_damage = 0


    def do(self, source, dest):
        return dest.receive_phisical_damage(self.calculate(source, dest))

    def calculate(self, source:Character, dest:Character) -> int:
        return max(self._base_damage + source.phisical_attack() - dest.phisical_resistence(), 0)

    def simulate(self, source:Character, dest:Character) -> str:
        return dest.name + "\n" + str(self.calculate(source, dest)) + ' phisical damage ' + "\n" + 'Prob ' + str(self._probability) + '%'

class SwordAttack(BasePhisicalAttack):
    _base_damage = 8
    _name = 'Sword attack'
    _probability = 80


class Destruction(BasePhisicalAttack):
    _base_damage = 12
    _name = 'Destruction'
    _probability = 20


class FireBall(BasePhisicalAttack):
    _base_damage = 5
    _name = 'Fire ball'
    _probability = 80

class BasePenalty(Action):
    _name = ''
    _base_damage = 0

    def do(self, source: Character, dest: Character):
        return dest.receive_magic_penalty(self.calculate(source, dest))

    def calculate(self, source:Character, dest:Character) -> int:
        return max(self._base_damage + source.magic_attack() - dest.magic_resistance(), 0)

    def simulate(self, source:Character, dest:Character) -> str:
        return str(self.calculate(source, dest)) + ' magic penalty ' + ' prob ' + str(self._probability) + '%'

class MagicPenalty(BasePenalty):

    _name = 'Magic penalty'
    _base_damage = 10
    _probability = 50

class ArmourPenalty(BasePenalty):
    _name = 'Armour penalty'
    _base_damage = 3
    _probability = 20
