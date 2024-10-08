import jsonpickle
import json


class Trait:
    def __init__(self, name: str, owner_stat_mods: dict, opponent_stat_mods,
                 description=None, awakened=False, parent_trait=None, awakening_chance=0.2, stars: int=1):
        """
        A Trait is a property of a Player that modifies the stats of the owner of the Trait and/or the opponent for the
        duration of a Combat Event. Each Trait is technically unique to each Player, though they may share names/characteristics
        with other Players' abilities.

        All Traits start as Dormant, not being applied during Events. However, during a Player's life, there is a chance
        for the Trait to Awaken. The Trait will then take effect.

        A Trait can either be Passive or Active. Passive Traits are applied during all Events, with no conditions.
        Active Traits, also known as "Abilities", have an activation_chance, where there is a random chance for it to
        activate for each Event.
        """

        self.name = name
        self.owner_stat_mods = owner_stat_mods
        self.opponent_stat_mods = opponent_stat_mods
        self.description = description
        self.awakened = awakened
        self.parent_trait = parent_trait
        self.awakening_chance = awakening_chance

    def awaken(self, owner):
        self.awakened = True

    def unawaken(self):
        self.awakened = False

    def serialize(self):
        return json.loads(jsonpickle.dumps(self, unpicklable=False))


class PassiveTrait(Trait):
    pass


class PermanentTrait(PassiveTrait):
    def __init__(self, name: str, stat_mods, description=None, awakened=False, parent_trait=None, awakening_chance=0.2):
        """
        A PassiveTrait which permanently changes the owner's stats. The key difference from a PassiveTrait is that a
        PermanentTrait does not change an opponent's stats. PassiveTraits only activate during Combat.
        More differences may be added in the future.
        :param name:
        :param stat_mods:
        :param description:
        :param awakened:
        :param parent_trait:
        :param awakening_chance:
        """
        self.name = name
        self.stat_mods = stat_mods
        self.description = description
        self.awakened = awakened
        self.parent_trait = parent_trait
        self.awakening_chance = awakening_chance

    def awaken(self, owner):
        self.awakened = True
        owner.apply_perm_trait(self)


class ActiveTrait(Trait):
    def __init__(self, name: str, owner_stat_mods: dict, opponent_stat_mods, activation_chance, awakened=False, parent_trait=None):
        super().__init__(name, owner_stat_mods, opponent_stat_mods, awakened, parent_trait)
        self.activation_chance = activation_chance
