import random
import numpy as np
from scipy.stats import dirichlet, multinomial, binom
import re


class Player:
    def __init__(self, player_name):
        self.name = player_name
        self.dice_number = 5
        self.current_roll = list()
        self.player_status = "in_game"
        self.bluff_factor = 0
        self.trust = {}

    def player_roll_result(self):
        """
        Simulate the roll of the number of dice for a player.
        The function update the roll dice of the player by modifying
        the attribute self.current_roll.
        """
        # initialization of the current_roll attribute
        self.current_roll = [0] * self.dice_number
        # simulation of the new roll of self.dice_number dices
        self.distrib = np.zeros(6)
        for i in range(self.dice_number):
            roll = random.randint(1, 6)
            self.current_roll[i] = roll
            self.distrib[roll - 1] += 1.0
        # no return because we updated the attribute self.current_roll

    def player_fails(self):
        """
        Update the attribute self.dice_number and self.player_status.
        If the player loose his last dice his status will be "disqualified".
        """
        self.dice_number -= 1
        print(self.name, "lost a dice !")
        if self.dice_number == 0:
            self.player_status = "disqualified"
            print(self.name, "is disqualified !")

    def player_wins_calza(self):
        """
        Update the attribute self.dice_number and self.player_status.
        If the player wins calza and have less than 5 dices, he wins a dice.
        """
        if self.dice_number < 5:
            self.dice_number += 1

    def make_choice(self, bets, dices):

        posteriors = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0]) / 6.0
        total_dices = sum(dices.values) - self.dice_number
        for bet in bets:
            player, bet = bet
            if player == self.name:
                continue
            nb, val = bets.split("d")
            nb = int(nb)
            val = int(val) - 1
            if player not in self.trust.keys():
                self.trust[player] = 1.0
            player_distrib = np.zeros(6)
            if val == 0:
                player_distrib[val] = nb
            else:
                player_distrib[val] = nb / 2.0
                player_distrib[0] = nb / 2.0
            # trust in palyer is temperature in softmax function
            player_distrib *= self.trust[player]
            player_distrib = np.exp(player_distrib)
            player_distrib /= player_distrib.sum()
            alpha = dices[player] / total_dices
            posteriors = posteriors * (1.0 - alpha) + player_distrib * alpha

        posteriors += self.distrib
        posteriors[1:] *= 2.0

        if len(bets) > 0:
            player, bet = bets[-1]
            nb, val = bets.split("d")
            nb = int(nb)
            val = int(val) - 1

            p = posteriors / posteriors.sum()
            prob_right = 1.0 - binom.cdf(
                min(nb, sum(dices.values)), sum(dices.values), p[val]
            )
            max_prob = 0.0
            max_val = None
            nb = None

            for i in range(val + 1, 6):
                prob_right_me = 1.0 - binom.cdf(
                    min(1, sum(dices.values)), sum(dices.values), p[i]
                )
                if prob_right_me > max_prob:
                    max_prob = prob_right_me
                    max_val = i
                    nb = 1

            for i in range(nb + 1, sum(dices.values)):
                for j in range(6):
                    prob_right_me = 1.0 - binom.cdf(
                        min(i, sum(dices.values)), sum(dices.values), p[j]
                    )
                    if prob_right_me > max_prob:
                        max_prob = prob_right_me
                        max_val = i
                        nb = 1

            # calculate superior value for each choice of overbet
            if np.max(posteriors) > prob_right:
                val_max = np.argmax(posteriors) + 1
                return "{nb}d{val}"
