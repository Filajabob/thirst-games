from game import Game
import utils
import time

print("Welcome to the Thirst Games.\n")

game = Game(utils.PlayerSet.load("assets/player_sets/JujutsuKaisen.json"), 2024)
game.start()

while game.can_run():
    outcome = game.rotate()
    print(f"{outcome.attacker.full_name} attacks {outcome.defender.full_name}")
    time.sleep(1)

    if outcome.result == utils.Outcome.ATTACKER_WIN:
        print(f"{outcome.attacker.full_name} kills {outcome.defender.full_name}")
    elif outcome.result == utils.Outcome.DEFENDER_WIN:
        print(f"{outcome.defender.full_name}, defending themself, kills {outcome.attacker.full_name}")
    else:
        print("Everyone runs away")

    time.sleep(1)

    print("")