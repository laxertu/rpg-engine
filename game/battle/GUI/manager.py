from game.battle.wrapper import BattleWrapper

class AbstractBattleManager:
    def __init__(self, team1: list, team2: list):
        bw = BattleWrapper(team1, team2)
        self.battle_wrapper = bw

    def next(self) -> bool:
        raise NotImplementedError('Abstract method')
