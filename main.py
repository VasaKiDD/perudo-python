import numpy as np
from src.perudo_game import PerudoGame
import time

if __name__ == "__main__":
    sleep_time = 0

    print("-----Welcome to the Perudo Game-----")

    players = 0
    while players > 5 or players < 1:
        players = int(input("How many AI player (Accepted answer: 1-5) ?\n"))
        print("AiPlayer number must be between 1-5")

    game = PerudoGame(players)
    game.play_game()
