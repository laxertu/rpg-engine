from game.prefabs.fantasy_game.battle import Battle
from easyAI import AI_Player


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
        self.is_current_player = False

    def __str__(self):
        result = ''
        result += self.name + ' [' + type(self).__name__+']'

        result += '[HP]: ' + str(self.pf())
        if self._armour_penalty:
            result += ' [ARMOUR PENALTY]'

        if self._magic_penalty:
            result += ' [MAGIC PENALTY]'

        return result + '           '

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

    def possible_moves(self, game: Battle):
        return self.abilities.keys()

    def scoring(self):
        return self.magic_resistance() + self.magic_attack() + self.phisical_resistence() + self.phisical_attack()


class HumanPlayer(Character):

    def ask_move(self, game: Battle):
        return None


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
        self._armour = 0
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


class BaseAction:
    _name = ''
    _probability = 0

    def probability(self):
        return self._probability

    def do(self, source: Character, dest: Character):
        return ''

    def __str__(self):
        return self._name + "\n" + 'Prob ' + str(self.probability()) + '% '

    def to_str(self):
        return str(self)

    def simulate(self, source:Character, dest:Character) -> str:
        return ''

    def get_name(self):
        return self._name

class NoneAction(BaseAction):
    def to_str(self):
        return ''

class BasePhisicalAttack(BaseAction):

    _name = ''
    _base_damage = 0


    def do(self, source, dest):
        return dest.receive_phisical_damage(self._base_damage + source.phisical_attack())

    def simulate(self, source:Character, dest:Character) -> str:
        return str(self._base_damage + source.phisical_attack()) + ' phisical damage ' + ' prob ' + str(self._probability) + '%'

class SwordAttack(BaseAction):
    _base_damage = 8
    _name = 'Sword attack'
    _probability = 70


class Destruction(BasePhisicalAttack):
    _name = 'Destruction'
    _probability = 20



class FireBall(BasePhisicalAttack):

    _name = 'Fire ball'
    _probability = 80

class BasePenalty(BaseAction):
    _name = ''
    _base_damage = 0

    def do(self, source: Character, dest: Character):
        return dest.receive_magic_penalty(self._base_damage + source.magic_attack())

    def simulate(self, source:Character, dest:Character) -> str:
        return str(self._base_damage + source.magic_attack()) + ' phisical damage ' + ' prob ' + str(self._probability) + '%'

class MagicPenalty(BasePenalty):

    _name = 'Magic penalty'
    _base_damage = 10
    _probability = 50

class ArmourPenalty(BasePenalty):
    _name = 'Armour penalty'
    _base_damage = 3
    _probability = 20
