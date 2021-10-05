import random


class AiPlayer:
    def __init__(self, player_name):
        self.player_name = player_name
        self.dice_number = 5
        self.current_roll = list()
        self.player_status = "in_game"
        self.bluff_factor = 0

    def player_roll_result(self):
        """
        Simulate the roll of the number of dice for a player.
        The function update the roll dice of the player by modifying
        the attribute self.current_roll.
        """
        # initialization of the current_roll attribute
        self.current_roll = [0] * self.dice_number
        # simulation of the new roll of self.dice_number dices
        for i in range(self.dice_number):
            roll = random.randint(1, 6)
            self.current_roll[i] = roll
        # no return because we updated the attribute self.current_roll

    def player_fails(self):
        """
        Update the attribute self.dice_number and self.player_status.
        If the player loose his last dice his status will be "disqualified".
        """
        self.dice_number -= 1
        if self.dice_number == 0:
            self.player_status = "disqualified"

    def make_choice(self, current_bet, state_of_game):
        """
        Compute the choice of the player, return either a new bet, "dudo" or "calza"
        :param
        """
        # TODO: code the decision making process for a player.




