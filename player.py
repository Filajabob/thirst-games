import utils


class Player:
    def __init__(self, given_name: str, surname: str, stats: dict, age: int, traits: list[utils.Trait]=[]):
        self.given_name = given_name
        self.surname = surname
        self.stats = stats
        self.age = age
        self.traits = traits

        if self.traits is not list[utils.Trait]:
            self.traits = [utils.Trait(**trait) for trait in self.traits]
                
        self.full_name = f"{self.given_name} {self.surname}"

    def serialize(self):
        return {
            "given_name": self.given_name,
            "surname": self.surname,
            "stats": self.stats,
            "age": self.age,
            "traits": [trait.serialize() for trait in self.traits]
        }

    def awakened_traits(self) -> list[utils.Trait]:
        """Returns a list of all awakened Traits that this Player has."""
        return [trait for trait in self.traits if trait.awakened]

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
