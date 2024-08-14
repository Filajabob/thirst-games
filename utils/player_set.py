import json
from player import Player


class PlayerSet:
    def __init__(self, players: list[Player]):
        """A set of Players for a Game"""
        self.players = players

    def kill(self, player: Player):
        """
        Removes a player from the PlayerSet. Do not remove directly from PlayerSet.players.
        """

        self.players.remove(player)

    def serialize(self, path=None):
        serialized_players = [player.serialize() for player in self.players]
        with open(path, 'w') as f:
            json.dump(serialized_players, f, indent=4)
            f.truncate()

        return serialized_players

    @staticmethod
    def load(path):
        with open(path, 'r') as f:
            serialized_players = json.load(f)

        players = [Player(**serialized_player) for serialized_player in serialized_players]

        return PlayerSet(players)
