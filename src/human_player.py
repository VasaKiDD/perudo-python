import random
import re

from src.player import Player


class Human(Player):
    def __init__(self):
        super(Human, self).__init__("")
        self.name = ""

    def get_name(self, ai_names):
        non_valid_name = True
        human_name = 0
        while non_valid_name:
            temp_name = input("Choose your player name: ")
            if len(temp_name) > 20:
                print("Your name is too long")
            elif temp_name in ai_names:
                print(
                    "already a player named like that, choose another "
                    "name please."
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

    def player_roll_result(self):
        dices_str = "Your dices are: "
        for i in range(self.dice_number):
            roll = random.randint(1, 6)
            dices_str += str(roll) + " "
            self.current_roll.append(roll)
        print(dices_str)

    def make_choice(self, bets, dices):
        """
        Compute the choice of the player, return either a new bet, "dudo"
        or "calza"
        """

        rule = "([0-9]+)d([0-9]+)"

        b = "First" if bets == [] else bets[-1]
        s = "Current Bet: {b}\n" "Current Dices: {d}".format(
            b=b, d=self.current_roll
        )
        print(s)

        if not bets:
            valid = True
            action = "accept"
        else:
            valid = False
            action = ""

        while not valid:
            question = (
                "What is your action ?\n"
                "Possible answers : dudo, calza or accept\n"
                "Answer:"
            )
            action = input(question)
            valid = (
                (action.lower() == "dudo")
                or (action.lower() == "calza")
                or (action.lower() == "accept")
            )
            if not valid:
                print("ActionError: action doesn't exist")

        bet = ""
        if action == "accept":
            valid = False
            while not valid:
                question = (
                    "What is your raise ? <number of dice>d<dice value>\n"
                    "Exemple: 5 dices of 6 <=> 5d6\n"
                    "Answer:"
                )
                bet = input(question)
                valid = re.match(rule, bet.lower()) is not None
                if valid and bets == []:
                    if int(bet.lower().split("d")[1]) == 1:
                        print("BetError: You can't start by betting dudos !")
                        valid = False
                if valid and int(bet.lower().split("d")[1]) > 6:
                    print("BetError: Max dice value is 6")
                    valid = False

        return action, bet
