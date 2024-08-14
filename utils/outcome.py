class Outcome:
    def __init__(self, attacker, defender, result):
        self.attacker = attacker
        self.defender = defender
        self.result = result

    DRAW = 0
    ATTACKER_WIN = 1
    DEFENDER_WIN = -1