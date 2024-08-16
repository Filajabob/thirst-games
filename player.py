import json
from typing import List, Dict
import utils
from constants import Constants

trait_module = __import__("utils.trait")


class Player:
    def __init__(self, given_name: str, surname: str, stats: dict, age: int, *, traits: List[utils.Trait]=[], raw_traits: Dict[str, List[Dict]]=None,
                 death_age: int=None, full_name=None, quotes: List[str]=[]):
        """

        :param given_name:
        :param surname:
        :param stats:
        :param age:
        :param traits: a dict of lists, seperated into the different types of Traits
        :param death_age:
        :param full_name:
        """
        self.given_name = given_name
        self.surname = surname
        self.stats = stats
        self.age = age
        self.traits = traits
        self.death_age = death_age
        self.quotes = quotes

        if raw_traits:
            for trait_type, trait_datas in raw_traits.items():
                for trait_data in trait_datas:
                    trait_cls = getattr(trait_module, trait_type)
                    self.traits.append(trait_cls(**trait_data))
                
        self.full_name = f"{self.given_name} {self.surname}"

    def serialize(self) -> dict:
        return {
            "given_name": self.given_name,
            "surname": self.surname,
            "stats": self.stats,
            "age": self.age,
            "death_age": self.death_age,
            "raw_traits": self.separate_serialize_traits()
        }

    def separate_serialize_traits(self) -> Dict[str, List[utils.Trait]]:
        separated_traits = {}
        print(self.traits)
        for trait in self.traits:
            if type(trait).__name__ not in separated_traits.keys():
                separated_traits[type(trait).__name__] = [trait.serialize()]
            else:
                separated_traits[type(trait).__name__].append(trait.serialize())

        return separated_traits

    def awakened_traits(self) -> list[utils.Trait]:
        """Returns a list of all awakened Traits that this Player has."""
        return [trait for trait in self.traits if trait.awakened]

    def dormant_traits(self) -> list[utils.Trait]:
        """Returns a list of all dormant (unawakened) Traits that this Player has."""
        return [trait for trait in self.traits if not trait.awakened]

    @staticmethod
    def adjust_stats(stats, trait_mods):
        """Adjusted a given dict of stats based on a list of Traits."""
        for trait_mods in trait_mods:
            for stat, adjustment in trait_mods.items():
                stats[stat] += adjustment

        return stats

    def stats_with_traits(self):
        """Returns the Player's stats, adjusted with Traits."""
        return self.adjust_stats(self.stats, [trait.owner_stat_mods for trait in self.awakened_traits()])

    def adjust_opponent_stats(self, opp_stats):
        """Returns an opponent's stats, adjusted with this Player's Traits"""
        return self.adjust_stats(opp_stats, [trait.opponent_stat_mods for trait in self.awakened_traits()])

    def apply_all_player_traits(self, opponent):
        """Returns the Player's Trait-adjusted stats, adjusted with an opponent's stats."""
        return self.adjust_stats(self.stats_with_traits(), [trait.opponent_stat_mods for trait in opponent.awakened_traits()])

    def apply_perm_trait(self, trait):
        """Applies a PermanentTrait to the Player's stats."""
        self.stats = self.adjust_stats(self.stats, trait.stat_mods)

    def apply_outcome_stat_changes(self, changes: dict, outcome: utils.Outcome):
        """Applies a given dict of percentages to stats. If positive, takes from the opponent. If negative, takes from self."""
        if outcome.attacker == self:
            opponent = outcome.defender
        else:
            opponent = outcome.attacker

        for stat, change in changes.items():
            if change > 0:
                self.stats[stat] += opponent.stats[stat] * change
            elif change < 0:
                self.stats[stat] += self.stats[stat] * change

    def apply_outcome_to_stats(self, outcome: utils.Outcome):
        """Based on an Outcome from a CombatEvent, apply changes to a Player's stats"""
        print(self.full_name, self.stats)
        if outcome.result:
            # Combat has ended, use Constants.OUTCOME_STAT_CHANGES
            if outcome.attacker == self:
                # I am the attacker
                changes = Constants.OUTCOME_STAT_CHANGES[outcome.result]["attacker"]
            else:
                # I am the defender
                changes = Constants.OUTCOME_STAT_CHANGES[outcome.result]["defender"]
        else:
            # Combat in progress, use Constants.NO_OUTCOME_STAT_CHANGES
            if outcome.attacker_failed():
                changes = Constants.NO_OUTCOME_STAT_CHANGES["attacker_fail"]
            else:
                changes = Constants.NO_OUTCOME_STAT_CHANGES["defender_fail"]

            if outcome.attacker == self:
                changes = changes["attacker"]
            else:
                changes = changes["defender"]

        self.apply_outcome_stat_changes(changes, outcome)

        print(self.full_name, self.stats)
