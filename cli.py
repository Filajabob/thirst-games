from game import Game
import utils
import time
from event import Event, CombatEvent, AwakeningEvent

print("Welcome to the Thirst Games.\n")

game = Game(utils.PlayerSet.load(f"assets/player_sets/{input('Insert Player Set Name: ')}.json"), 2024)
game.start()

while game.can_run():
    print(f"Year: {game.year}\n")
    events = game.rotate()

    for event in events:
        if isinstance(event, CombatEvent):
            if not game.can_run():
                break
            event.start()
            utils.typewrite(event.start_message())
            while True:
                outcome = event.rotate()

                utils.typewrite(outcome.combat_result_msg())

                if outcome.awakening:
                    utils.typewrite(f"{outcome.winner().full_name} is having an Awakening!")
                    awakening_event = AwakeningEvent(outcome.winner())
                    awakened_trait = awakening_event.start()

                    if awakened_trait:
                        utils.typewrite(f"{outcome.winner().full_name} had Awakened '{awakened_trait.name}'!")
                        utils.typewrite(awakened_trait.description)
                    else:
                        utils.typewrite("The Awakening failed.")

                if outcome.result is not utils.Outcome.NO_OUTCOME:
                    break

            print("")

utils.typewrite(f"{game.player_set.players[0].full_name} is the winner of the Thirst Games!")