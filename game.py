import random
from event import Event, CombatEvent
import utils


class Game:
    def __init__(self, player_set: utils.PlayerSet, year):
        self.player_set = player_set
        self.year = year

    def start(self):
        pass

    def rotate(self):
        """
        Advances to the next year and does a random amount of events.
        :return:
        """

        # into CombatEvent
        self.year += 1

        for player in self.player_set.players:
            player.age += 1

        players = random.sample(self.player_set.players, 2)
        combat_event = CombatEvent(*players,
                                   self.player_set)  # Get two random, unique players and input
        return utils.Outcome(players[0], players[1], combat_event.calculate())

    def can_run(self):
        return len(self.player_set.players) >= 2
