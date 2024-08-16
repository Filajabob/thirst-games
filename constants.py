import json

class Constants:
    # Applies changes proportionally based on opponent's stats. If negative, applies changes based on own stats.
    OUTCOME_STAT_CHANGES = {
        2: {  # attacker win
            "attacker": {
                "attack": 0.03,
                "resolve": 0.01
            },
            "defender": {}
        },
        1: {  # defender flees
            "attacker": {
                "attack": 0.01,
                "resolve": 0.02
            },
            "defender": {
                "defense": -0.01,
                "resolve": -0.02
            }
        },
        0: {  # draw
            "attacker": {},
            "defender": {}
        },
        -1: {  # attacker flees
            "attacker": {
                "attack": -0.01,
                "resolve": -0.02
            },
            "defender": {
                "defense": 0.01,
                "resolve": 0.02
            }
        },
        -2: {  # defender win
            "attacker": {},
            "defender": {
                "defense": 0.03,
                "resolve": 0.01
            }
        }
    }

    NO_OUTCOME_STAT_CHANGES = {
        "attacker_fail": {
            "attacker": {
                "attack": -0.005,
                "resolve": -0.01
            },
            "defender": {
                "defense": 0.005,
                "resolve": 0.01
            }
        },
        "defender_fail": {
            "attacker": {
                "attack": 0.005,
                "resolve": 0.01
            },
            "defender": {
                "defense": -0.005,
                "resolve": -0.01
            }
        }
    }

    MESSAGES_JSON = "assets/announcements.json"  # where to pull announcement messages from

    ANNUAL_EVENTS_LOWER_BOUND = 1
    ANNUAL_EVENTS_UPPER_BOUND = 3

    with open(MESSAGES_JSON, 'r') as f:
        MESSAGES = json.load(f)

    BASE_AWAKENING_CHANCE = 0.2  # After killing an opponent, the chance of an AwakeningEvent

    TRAIT_STEAL_CHANCE = 0.05  # After killing an opponent, the chance of stealing a Trait

    DEATH_EVENT_CHANCE = 0.1  # The chance we should have a NaturalDeathEvent.
    DEATH_EVENT_DEATH_RATE = 0.1  # After starting a DeathEvent, the chance of dying
