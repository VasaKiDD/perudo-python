import argparse

from src.perudo_game import PerudoGame

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--no-human", action="store_true")
    parser.add_argument("--players", type=int, default=6)

    sleep_time = 0

    args = parser.parse_args()

    if args.no_human:
        game = PerudoGame(args.players, no_human=True)
        game.play_game()

    else:
        print("-----Welcome to the Perudo Game-----")

        players = 0
        while players > 5 or players < 1:
            players = int(
                input("How many AI player (Accepted answer: 1-5) ?\n")
            )
            print("AiPlayer number must be between 1-5")

        game = PerudoGame(players)
        game.play_game()
