import time
import random


class Human:
    def __init__(self):
        self.name = "Napoleon"
        self.dice_number = 5
        self.current_roll = list()
        self.player_status = "in_game"
        self.current_bet = "0d0"

    def get_name(self, ai_names):
        non_valid_name = True
        human_name = 0
        while non_valid_name:
            temp_name = input("Choose your player name: ")
            if len(temp_name) > 20:
                print("Your name is too long")
            elif temp_name in ai_names:
                print(
                    "already a player named like that, choose another name please."
                )
            else:
                human_name = temp_name
                non_valid_name = False
        else:
            self.name = human_name
            print(
                "Your name is {}, have a good game {}!".format(
                    human_name, human_name
                )
            )

    def get_human_roll(self):
        print("Rolling your dices...")
        time.sleep(5)
        for i in range(self.dice_number):
            roll = random.randint(1, 6)
            self.current_roll.append(roll)

    def player_fails(self):
        """
        Update the attribute self.dice_number and self.player_status.
        If the player loose his last dice his status will be "disqualified".
        """
        self.dice_number -= 1
        if self.dice_number == 0:
            self.player_status = "disqualified"

    def player_wins_calza(self):
        """
        Update the attribute self.dice_number and self.player_status.
        If the player wins calza and have less than 5 dices, he wins a dice.
        """
        if self.dice_number < 5:
            self.dice_number += 1

    def make_choice(self, current_bet, last_player):
        """
        Compute the choice of the player, return either a new bet, "dudo" or "calza"
        """
