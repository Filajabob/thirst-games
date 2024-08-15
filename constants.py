import json


class Constants:
    ATTACKER_WIN_STAT_BOOST = 0.01
    DEFENDER_WIN_STAT_BOOST = 0.01

    FAIL_STAT_PENALTY = 0.01  # penalty to statsfor fleeing or failing

    MESSAGES_JSON = "assets/announcements.json"  # where to pull announcement messages from

    ANNUAL_EVENTS_LOWER_BOUND = 2
    ANNUAL_EVENTS_UPPER_BOUND = 6

    with open(MESSAGES_JSON, 'r') as f:
        MESSAGES = json.load(f)

    BASE_AWAKENING_CHANCE = 1
