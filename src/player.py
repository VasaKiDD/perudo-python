import random
import numpy as np
from scipy.stats import binom


class Player:
    def __init__(self, player_name):
        self.name = player_name
        self.dice_number = 5
        self.current_roll = list()
        self.player_status = "in_game"
        self.trust = {}
        self.risk_taking = 1.0
        self.bluff_factor = 1.0
        self.init_trust = 20.0
        self.tilt_gamma = 0.95
        self.distrib = np.zeros(6)

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
        self.distrib /= self.distrib.sum()
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
        self.risk_taking *= self.tilt_gamma

    def player_wins_calza(self):
        """
        Update the attribute self.dice_number and self.player_status.
        If the player wins calza and have less than 5 dices, he wins a dice.
        """
        if self.dice_number < 5:
            print(self.name, "wins a dice !")
            self.dice_number += 1

    @staticmethod
    def calculate_probs(val, nb, total_dices, distribution):
        probs = []

        if val != 0:
            for j in range(nb // 2 + 1, total_dices + 1):
                p = 1.0 - binom.cdf(j, total_dices, distribution[0])
                probs.append([j, 0, p])
            if nb + 1 <= total_dices:
                for j in range(nb + 1, total_dices + 1):
                    p = 1.0 - binom.cdf(j, total_dices, distribution[val])
                    probs.append([j, val, p])
            for i in range(val + 1, 6):
                for j in range(1, total_dices + 1):
                    p = 1.0 - binom.cdf(j, total_dices, distribution[i])
                    probs.append([j, i, p])
        else:
            if nb + 1 <= total_dices:
                for j in range(nb + 1, total_dices + 1):
                    p = 1.0 - binom.cdf(j, total_dices, distribution[0])
                    probs.append([j, 0, p])
            if nb * 2 + 1 <= total_dices:
                for i in range(1, 6):
                    for j in range(nb * 2 + 1, total_dices + 1):
                        p = 1.0 - binom.cdf(j, total_dices, distribution[i])
                        probs.append([j, i, p])

        probs = np.array(probs)
        return probs

    def make_choice(self, bets, dices):

        total_dices = sum(dices.values())
        posteriors = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0]) / 6.0
        p_total_dices = total_dices - self.dice_number
        for bet in bets:
            player, bet = bet
            if player == self.name:
                continue
            nb, val = bet.split("d")
            nb = int(nb)
            val = int(val) - 1
            if player not in self.trust.keys():
                self.trust[player] = self.init_trust
            player_distrib = np.zeros(6)
            if val == 0:
                player_distrib[val] = nb
            else:
                player_distrib[val] = nb / 2.0
                player_distrib[0] = nb / 2.0
            # trust in player is temperature in softmax function
            player_distrib *= self.trust[player]
            player_distrib = np.exp(player_distrib)
            player_distrib /= player_distrib.sum()
            alpha = dices[player] / p_total_dices
            posteriors = posteriors * (1.0 - alpha) + player_distrib * alpha

        alpha = dices[self.name] / total_dices
        posteriors = posteriors * (1.0 - alpha) + self.distrib * alpha
        # print(posteriors)
        posteriors[1:] *= 2.0
        distribution = posteriors / posteriors.sum()

        if len(bets) > 0:
            _, bet = bets[-1]
            nb, val = bet.split("d")
            nb = int(nb)
            val = int(val) - 1

            prob_opp_wrong = binom.cdf(
                min(nb, total_dices), total_dices, distribution[val]
            )

            # Calza Decision
            sum_probs = 0
            for i in range(nb):
                p1 = binom.pmf(i, total_dices, distribution[val])
                p2 = 1.0 - binom.cdf(nb - i, total_dices, distribution[0])
                sum_probs += p1 * p2

            if sum_probs > self.risk_taking:
                return "calza", None

            probs = self.calculate_probs(val, nb, total_dices, distribution)

            # Bluff Decision
            utility = (
                probs[:, 0] / total_dices + probs[:, 1] / 6 + probs[:, 2]
            ) / 3.0
            max_utility = np.argmax(utility)
            if utility.max() > self.bluff_factor:
                # print("=====================> Bluff", utility.max())
                my_bet = (
                    str(int(probs[max_utility, 0]))
                    + "d"
                    + str(int(probs[max_utility, 1] + 1))
                )
                return "accept", my_bet

            # Rational Decision
            max_win_arg = np.argmax(probs[:, 2])
            if (
                probs[max_win_arg, 2] > prob_opp_wrong
                or prob_opp_wrong < self.risk_taking
            ):
                my_bet = (
                    str(int(probs[max_win_arg, 0]))
                    + "d"
                    + str(int(probs[max_win_arg, 1] + 1))
                )
                return "accept", my_bet
            else:
                return "dudo", None
        else:
            probs = self.calculate_probs(1, 0, total_dices, distribution)

            # Bluff Decision
            utility = (
                probs[:, 0] / total_dices + probs[:, 1] / 6 + probs[:, 2]
            ) / 3.0
            utility /= 3
            args_utility = np.argsort(utility)
            if probs[args_utility[-1], 1] == 0:
                max_utility = args_utility[-2]
            else:
                max_utility = args_utility[-1]
            if utility.max() > self.bluff_factor:
                # print("=====================> Bluff", utility.max())
                my_bet = (
                    str(int(probs[max_utility, 0]))
                    + "d"
                    + str(int(probs[max_utility, 1] + 1))
                )
                return "accept", my_bet

            # Rationnal Decision
            args_probs = np.argsort(probs[:, 2])
            if probs[args_probs[-1], 1] == 0:
                max_win_arg = args_probs[-2]
            else:
                max_win_arg = args_probs[-1]
            my_bet = (
                str(int(probs[max_win_arg, 0]))
                + "d"
                + str(int(probs[max_win_arg, 1] + 1))
            )
            return "accept", my_bet
