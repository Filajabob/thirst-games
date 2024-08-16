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

    ANNUAL_EVENTS_LOWER_BOUND = 2
    ANNUAL_EVENTS_UPPER_BOUND = 6

    with open(MESSAGES_JSON, 'r') as f:
        MESSAGES = json.load(f)

    BASE_AWAKENING_CHANCE = 0.25
