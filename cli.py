from game import Game
import utils
import time
from event import Event, CombatEvent

print("Welcome to the Thirst Games.\n")

game = Game(utils.PlayerSet.load(input("Insert Player Set path: ")), 2024)
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
            time.sleep(1)
            while True:
                outcome = event.rotate()

                utils.typewrite(outcome.combat_result_msg())
                time.sleep(1)

                if outcome.result is not utils.Outcome.NO_OUTCOME:
                    time.sleep(2)
                    break

            print("")

utils.typewrite(f"{game.player_set.players[0].full_name} is the winner of the Thirst Games!")