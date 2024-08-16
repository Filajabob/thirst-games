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

    def outcome(self, result: int, *, awakening=False) -> Outcome:
        outcome = Outcome(self.attacker, self.defender, result, self.turn, awakening=awakening)

        self.attacker.apply_outcome_to_stats(outcome)
        self.defender.apply_outcome_to_stats(outcome)

        return outcome

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

        attacker_adjusted_stats = self.attacker.apply_all_player_traits(self.defender)
        defender_adjusted_stats = self.defender.apply_all_player_traits(self.attacker)

        if self.turn % 2 == 0:
            # Turn is even, therefore the attacker is attacking.
            attacker_atk_effect = attacker_adjusted_stats["attack"] - defender_adjusted_stats["defense"]

            # Ensure attacker doesn't flee immediately (that would be sad)
            if self.turn != 0:
                if not utils.random_weighted_boolean((attacker_adjusted_stats["resolve"] + attacker_atk_effect) / 2):
                    return self.outcome(Outcome.ATTACKER_FLEES)  # Attacker flees

            if utils.random_weighted_boolean(attacker_atk_effect):
                # The attacker kills the defender
                self.player_set.kill(self.defender)

                if utils.random_weighted_boolean(Constants.BASE_AWAKENING_CHANCE):
                    return self.outcome(Outcome.ATTACKER_WIN, awakening=True)
                else:
                    return self.outcome(Outcome.ATTACKER_WIN)
        else:
            # Turn is odd, therefore the defender is attacking
            defender_atk_effect = defender_adjusted_stats["attack"] - attacker_adjusted_stats["defense"]
            if not utils.random_weighted_boolean((defender_adjusted_stats["resolve"] + defender_atk_effect) / 2):
                return self.outcome(Outcome.DEFENDER_FLEES)  # Defender flees

            if utils.random_weighted_boolean(defender_atk_effect):
                # The defender kills the attacker
                self.player_set.kill(self.attacker)

                if utils.random_weighted_boolean(Constants.BASE_AWAKENING_CHANCE):
                    return self.outcome(Outcome.DEFENDER_WIN, awakening=True)
                else:
                    return self.outcome(Outcome.DEFENDER_WIN)

        return self.outcome(Outcome.NO_OUTCOME)  # If we reach this point, no one won or fled, so we continue.


class PersonalEvent(Event):
    pass


class AwakeningEvent(PersonalEvent):
    def __init__(self, awakening_player):
        self.awakening_player = awakening_player

    def start(self):
        for trait in self.awakening_player.dormant_traits():
            if utils.random_weighted_boolean(trait.awakening_chance):
                trait.awaken(self.awakening_player)

                return trait


class NaturalDeathEvent(PersonalEvent):
    def __init__(self, player_set):
        super().__init__(player_set)
        self.player = None

    def start(self):
        """Returns True if the player dies to natural causes."""
        elderly_players = self.player_set.elderly_players()
        if elderly_players:
            sick_player = random.choice(elderly_players)

        self.player = sick_player

        if utils.random_weighted_boolean(Constants.DEATH_EVENT_DEATH_RATE):
            self.player_set.kill(sick_player)
            return True
        else:
            return False


class MatingEvent(Event):
    pass
