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

    def stats_with_traits(self):
        """Returns the Player's stats, adjusted with Traits."""
        adjusted_stats = self.stats

        for trait in self.awakened_traits():
            for stat, adjustment
