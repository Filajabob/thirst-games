import json
import random
from constants import Constants

with open(Constants.MESSAGES_JSON, 'r') as f:
    messages = json.load(f)


class Outcome:
    def __init__(self, attacker, defender, result: int, turn: int, awakening: bool=False):
        """
        Object that represents the outcome of a game.Game rotation
        :param attacker: player.Player: The attacker of a CombatEvent
        :param defender: player.Player: The defender of a CombatEvent
        :param result: int: An integer representing who won; 0 is a draw, 1 is an attacker win, -1 is a defender win
        :param awakening: bool: Whether the winner (if any) can have a chance to Awaken.
        """
        self.attacker = attacker
        self.defender = defender
        self.result = result
        self.turn = turn
        self.awakening = awakening

    def winner(self):
        if self.result > 0:
            return self.attacker
        elif self.result < 0:
            return self.defender
        else:
            return None

    def insert_names(self, msg):
        msg = msg.replace('{a}', self.attacker.full_name)
        msg = msg.replace('{d}', self.defender.full_name)

        msg = msg.replace('{af}', self.attacker.given_name)
        msg = msg.replace('{al}', self.attacker.surname)

        msg = msg.replace('{df}', self.defender.given_name)
        msg = msg.replace('{dl}', self.defender.surname)

        return msg

    def combat_result_msg(self):
        """Generates a message for the result of Combat"""
        if self.result == self.ATTACKER_WIN:
            raw_msg = random.choice(messages["outcomes"]["attacker_win"])
        elif self.result == self.DEFENDER_WIN:
            raw_msg = random.choice(messages["outcomes"]["defender_win"])
        elif self.result == self.ATTACKER_FLEES:
            raw_msg = random.choice(messages["outcomes"]["attacker_flees"])
        elif self.result == self.DEFENDER_FLEES:
            raw_msg = random.choice(messages["outcomes"]["defender_flees"])
        elif self.result is self.NO_OUTCOME:
            if self.turn % 2 == 0:
                raw_msg = random.choice(messages["outcomes"]["no_outcome"]["attackers_turn"])
            else:
                raw_msg = random.choice(messages["outcomes"]["no_outcome"]["defenders_turn"])
        else:
            raw_msg = random.choice(messages["outcomes"]["draw"])

        return self.insert_names(raw_msg)

    def attacker_failed(self) -> bool:
        if self.result is self.NO_OUTCOME and self.turn % 2 == 0:
            return True
        else:
            return False

    def defender_failed(self) -> bool:
        if self.result is self.NO_OUTCOME and self.turn % 2 == 1:
            return True
        else:
            return False


    DRAW = 0

    ATTACKER_FLEES = -1
    DEFENDER_FLEES = 1

    ATTACKER_WIN = 2
    DEFENDER_WIN = -2

    NO_OUTCOME = None
