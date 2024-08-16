import json
import numpy as np
import random
from player import Player
import utils

rng = np.random.default_rng()

with open("assets/templates/traits.json", 'r') as f:
    trait_templates = json.load(f)


def normal():
    num = rng.normal(0.5, 0.15)

    if num > 1:
        return 1
    elif num < 0:
        return 0

    return num


players = []

print("Leave blank and press enter to quit.")
while True:
    given_name = input("\nGiven Name: ")

    if given_name == '':
        break

    surname = input("Surname: ")

    traits = []

    while True:
        trait_name = input("Insert trait name (leave blank to exit): ")

        if trait_name == '':
            break

        if trait_name == "random":
            trait_type = random.choice(["PassiveTrait", "PermanentTrait"])
            traits_set = trait_templates[trait_type]

            if trait_type == "PassiveTrait":
                traits.append(utils.PassiveTrait(**random.choice(list(traits_set.values()))))
            else:
                traits.append(utils.PermanentTrait(**random.choice(list(traits_set.values()))))

            break

        trait_type = input("Insert trait type (i.e. PassiveTrait): ")
        trait_data = trait_templates[trait_type][trait_name]

        if trait_type == "PassiveTrait":
            traits.append(utils.PassiveTrait(**trait_data))
        elif trait_type == "PermanentTrait":
            traits.append(utils.PermanentTrait(**trait_data))

    players.append(Player(
        given_name, surname, {
            "attack": normal(),
            "defense": normal(),
            "resolve": normal()
        }, rng.normal(30, 3), traits=traits, death_age=round(rng.normal(70, 3))
    )
    )

player_set = utils.PlayerSet(players)
player_set.serialize(f"assets/player_sets/{input('Name this Player Set: ')}.json")
