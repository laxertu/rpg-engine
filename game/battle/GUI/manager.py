
class AbstractBattleManager:
    def __init__(self, team1, team2):
        pass

    def next(self) -> bool:
        raise NotImplementedError('Abstract method')
