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
    name = ''
    desc = ''

    def probability(self):
        return 0

    def do(self, source: Character, dest: Character):
        return ''

    def __str__(self):
        return self.name + "\n" + 'Prob ' + str(self.probability()) + '% ' + self.desc

    def to_str(self):
        return str(self)

class NoneAction(BaseAction):
    def to_str(self):
        return ''


class SwordAttack(BaseAction):

    name = 'Sword attack'
    desc = 'Base 8 ph damage'

    def probability(self):
        return 70

    def do(self, source, dest):
        return dest.receive_phisical_damage(8 + source.phisical_attack())


class Destruction(BaseAction):
    name = 'Destruction'
    desc = 'Base 12 ph damage'

    def probability(self):
        return 20

    def do(self, source: Character, dest: Character):
        return dest.receive_phisical_damage(12 + source.phisical_attack())


class FireBall(BaseAction):

    name = 'Fire ball'
    desc = 'Base 8 ph damage'

    def probability(self):
        return 80

    def do(self, source: Character, dest: Character):
        return dest.receive_magic_damage(8 + source.magic_attack())


class MagicPenalty(BaseAction):

    name = 'Magic penalty'
    desc = 'Base 8 ph damage'

    def probability(self):
        return 50

    def do(self, source: Character, dest: Character):
        return dest.receive_magic_penalty(8 + source.magic_attack())


class ArmourPenalty:
    name = 'Armour penalty'
    desc = 'Base 3 base armour penalty'

    def probability(self):
        return 20

    def do(self, source: Character, dest: Character):
        return dest.receive_armour_penalty(3 + source.magic_attack())
