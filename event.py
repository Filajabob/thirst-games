import player
import random
from constants import Constants
import utils



class Event:
    def __init__(self, player_set: utils.PlayerSet):
        self.player_set = player_set


class CombatEvent(Event):
    def __init__(self, attacker, defender, player_set: utils.PlayerSet):
        self.attacker = attacker
        self.defender = defender
        self.player_set = player_set

    def calculate(self):
        """Determines the outcome of the Event."""

        # Attacker will attack the defender first
        # The higher the attack_effect, the more likely the attacker will kill successfully
        attack_effect = self.attacker.stats["attack"] - self.defender.stats["defense"]

        if utils.random_weighted_boolean(attack_effect):
            # ATTACKER WIN - Attacker kills defender
            self.attacker.stats["attack"] += Constants.ATTACKER_WIN_STAT_BOOST
            self.attacker.stats["resolve"] += Constants.ATTACKER_WIN_STAT_BOOST

            self.player_set.kill(self.defender)

            return utils.Outcome.ATTACKER_WIN
        else:
            counterattack_effect = self.defender.stats["attack"] - self.attacker.stats["defense"]

            # Takes the average of the defender's advantage and their resolve, then uses that to calculate the chance
            # of fleeing (ie. if a defender is kind of strong compared to the attacker, but is scared AF,
            # they'd probably run)
            if utils.random_weighted_boolean((self.defender.stats["resolve"] + counterattack_effect) / 2):
                # Defender attacks back
                if utils.random_weighted_boolean(counterattack_effect):
                    # DEFENDER WIN - Defender kills attacker
                    self.defender.stats["attack"] += Constants.DEFENDER_WIN_STAT_BOOST
                    self.defender.stats["resolve"] += Constants.DEFENDER_WIN_STAT_BOOST

                    self.player_set.kill(self.attacker)

                    return utils.Outcome.DEFENDER_WIN

                # DRAW - Everyone flees (nothing happens)
                self.attacker.stats["resolve"] -= Constants.FLEE_RESOLVE_PENALTY
                self.defender.stats["resolve"] -= Constants.FLEE_RESOLVE_PENALTY

            return utils.Outcome.DRAW
