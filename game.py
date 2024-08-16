import random
from event import Event, CombatEvent, NaturalDeathEvent
import utils
from constants import Constants


class Game:
    def __init__(self, player_set: utils.PlayerSet, year):
        self.player_set = player_set
        self.year = year

    def start(self):
        pass

    def rotate(self) -> list[Event]:
        """
        Advances to the next year and returns a random amount of Events.
        :return:
        """

        self.year += 1

        for player in self.player_set.players:
            player.age += 1

        events = []

        for _ in range(random.randint(Constants.ANNUAL_EVENTS_LOWER_BOUND, Constants.ANNUAL_EVENTS_UPPER_BOUND)):
            if utils.random_weighted_boolean(Constants.DEATH_EVENT_CHANCE):
                events.append(NaturalDeathEvent(self.player_set))
                continue

            events.append(CombatEvent(self.player_set))  # more event types to be added

        return events

    def can_run(self):
        return len(self.player_set.players) >= 2
