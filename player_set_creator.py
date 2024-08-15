import numpy as np
from player import Player
import utils

rng = np.random.default_rng()


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

    players.append(Player(
        given_name, surname, {
            "attack": normal(),
            "defense": normal(),
            "resolve": normal()
        }, 18, traits=[utils.PassiveTrait("Natural Experience", {"resolve": 0.2}, {}, )]
    )
    )

player_set = utils.PlayerSet(players)
player_set.serialize(f"assets/player_sets/{input('Name this Player Set: ')}.json")
