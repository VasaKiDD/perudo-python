import numpy as np
import time

if __name__ == "__main__":
    print("-----Welcome to the Perudo Game-----")

    players = 0
    while players > 5 or players < 1:
        players = input("How many AI player (Accepted answer: 1-5) ?\n")
        print("AiPlayer number must be between 1-5")

    dices = {}
    for i in range(players):
        dices[i] = 5

    print("The game is starting.\n")
    print("Coosing randomly starting player.\n")
    starting_player = np.random.randint(players)
    if starting_player > 0:
        print("AiPlayer {s} is starting")
    else:
        print("You start")
