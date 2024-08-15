import player
import random
from constants import Constants
import utils
from utils import Outcome


class Event:
    def __init__(self, player_set: utils.PlayerSet):
        """
        Events are the building blocks of a Game - they cover all the interesting things in a Game like Combat, Awakenings, etc.
        :param player_set: The Player Set to pull Players from to use in Events.
        """
        self.player_set = player_set

    def start(self):
        pass


class CombatEvent(Event):
    def __init__(self, player_set: utils.PlayerSet):
        """
        An Event that involves two Players. One Player is the 'attacker' doing the first attack. Using both Players'
        stats, a result is randomly determined. If the attacker 'wins' (kills the defender), the Combat Event is over.
        However, if the attacker fails, the defender will have a choice to attack back or flee. The same thing is
        randomly determined (based on stats). This continues until either someone dies or flees, or if a limit is
        reached (where both Players flee).

        CombatEvent.attacker and CombatEvent.defender remains the same throughout the Combat Event.

        :param player_set: The set to pull Players from and to remove Players from.
        """
        self.player_set = player_set
        self.attacker = None
        self.defender = None
        self.turn = -1

    def start(self):
        """Generates players and does other tasks required before starting the Event."""
        players = random.sample(self.player_set.players, 2)

        self.attacker = players[0]
        self.defender = players[1]

    def outcome(self, result: int) -> Outcome:
        return Outcome(self.attacker, self.defender, result, self.turn)

    def insert_names(self, msg):
        msg = msg.replace('{a}', self.attacker.full_name)
        msg = msg.replace('{d}', self.defender.full_name)

        msg = msg.replace('{af}', self.attacker.given_name)
        msg = msg.replace('{al}', self.attacker.surname)

        msg = msg.replace('{df}', self.defender.given_name)
        msg = msg.replace('{dl}', self.defender.surname)

        return msg

    def start_message(self):
        raw_msg = random.choice(Constants.MESSAGES["general"]["combat_start"])
        return self.insert_names(raw_msg)

    def rotate(self) -> Outcome:
        """Rotates to the next turn."""
        self.turn += 1
        if self.turn % 2 == 0:
            # Turn is even, therefore the attacker is attacking.
            attacker_atk_effect = self.attacker.stats["attack"] - self.defender.stats["defense"]

            # Ensure attacker doesn't flee immediately (that would be sad)
            if self.turn != 0:
                if not utils.random_weighted_boolean((self.attacker.stats["resolve"] + attacker_atk_effect) / 2):
                    return self.outcome(Outcome.ATTACKER_FLEES)  # Attacker flees

            if utils.random_weighted_boolean(attacker_atk_effect):
                # The attacker kills the defender
                self.player_set.kill(self.defender)
                return self.outcome(Outcome.ATTACKER_WIN)
        else:
            # Turn is odd, therefore the defender is attacking
            defender_atk_effect = self.defender.stats["attack"] - self.attacker.stats["defense"]
            if not utils.random_weighted_boolean((self.defender.stats["resolve"] + defender_atk_effect) / 2):
                return self.outcome(Outcome.DEFENDER_FLEES)  # Defender flees

            if utils.random_weighted_boolean(defender_atk_effect):
                # The defender kills the attacker
                self.player_set.kill(self.attacker)
                return self.outcome(Outcome.DEFENDER_WIN)

        return self.outcome(Outcome.NO_OUTCOME)  # If we reach this point, no one won or fled, so we continue.

    # def calculate(self):
    #     """Determines the outcome of the Event."""
    #
    #     # Attacker will attack the defender first
    #     # The higher the attack_effect, the more likely the attacker will kill successfully
    #     attack_effect = self.attacker.stats["attack"] - self.defender.stats["defense"]
    #
    #     if utils.random_weighted_boolean(attack_effect):
    #         # ATTACKER WIN - Attacker kills defender
    #         self.attacker.stats["attack"] += Constants.ATTACKER_WIN_STAT_BOOST
    #         self.attacker.stats["resolve"] += Constants.ATTACKER_WIN_STAT_BOOST
    #
    #         self.player_set.kill(self.defender)
    #
    #         return utils.Outcome.ATTACKER_WIN
    #     else:
    #         # ATTACKER FAILED - DEFENDER CAN COUNTERATTACK OR FLEE
    #         self.attacker.stats["attack"] -= Constants.FAIL_STAT_PENALTY  # Attacker gets a bit worse at attacking
    #         counterattack_effect = self.defender.stats["attack"] - self.attacker.stats["defense"]
    #
    #         # Takes the average of the defender's advantage and their resolve, then uses that to calculate the chance
    #         # of fleeing (i.e. if a defender is kind of strong compared to the attacker, but is scared AF,
    #         # they'd probably run)
    #         if utils.random_weighted_boolean((self.defender.stats["resolve"] + counterattack_effect) / 2):
    #             # DEFENDER COUNTERATTACKS
    #             if utils.random_weighted_boolean(counterattack_effect):
    #                 # DEFENDER WIN - Defender kills attacker
    #                 self.defender.stats["attack"] += Constants.DEFENDER_WIN_STAT_BOOST
    #                 self.defender.stats["defense"] += Constants.DEFENDER_WIN_STAT_BOOST
    #                 self.defender.stats["resolve"] += Constants.DEFENDER_WIN_STAT_BOOST
    #
    #                 self.player_set.kill(self.attacker)
    #
    #                 return utils.Outcome.DEFENDER_WIN
    #             else:
    #                 # DEFENDER FAILS COUNTERATTACK - EVERYONE FLEES
    #                 self.defender.stats["attack"] -= Constants.FAIL_STAT_PENALTY
    #         else:
    #             # DEFENDER FLEES WITHOUT COUNTERATTACKING
    #             pass
    #
    #         # DRAW - Everyone flees (nothing happens)
    #         self.attacker.stats["resolve"] -= Constants.FAIL_STAT_PENALTY
    #         self.defender.stats["resolve"] -= Constants.FAIL_STAT_PENALTY
    #
    #         return utils.Outcome.DRAW
