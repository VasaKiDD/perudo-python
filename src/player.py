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
        self.risk_taking = random.random()
        self.bluff_factor = random.random() * 0.5
        self.init_trust = 25.0 * random.random()
        self.tilt_gamma = 0.9
        self.trust_loss = 0.5
        self.distrib = np.zeros(6)
        self.posteriors = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0]) / 6.0

    def player_roll_result(self):
        """
        Simulate the roll of the number of dice for a player.
        The function update the roll dice of the player by modifying
        the attribute self.current_roll.
        """
        # initialization of the current_roll attribute
        self.current_roll = []
        # simulation of the new roll of self.dice_number dices
        self.distrib = np.zeros(6)
        for i in range(self.dice_number):
            roll = random.randint(1, 6)
            self.current_roll.append(roll)
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
        """
        This is the mathematical/AI decision part of an AI player with
        bayesian reasonning, expectation maximisation and bluff.
        """
        total_dices = sum(dices.values())
        p_total_dices = total_dices - self.dice_number
        prior = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0]) / 6.0
        posteriors_player = []
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
                player_distrib[val] = 2 * nb
                player_distrib[0] = nb
            # trust in player is temperature in softmax function
            player_distrib *= self.trust[player]
            player_distrib = np.exp(player_distrib)
            player_distrib /= player_distrib.sum()
            alpha = dices[player] / p_total_dices
            post = prior * (1.0 - alpha) + player_distrib * alpha
            posteriors_player.append(post)

        if posteriors_player:
            posteriors = np.array(posteriors_player).sum(0)
            self.posteriors = posteriors / posteriors.sum()
        else:
            self.posteriors = prior

        # bluff part
        if random.random() < self.bluff_factor:
            distrib = np.array([5, 0, 1, 2, 3, 4])
            distrib = np.exp(distrib) / np.exp(distrib).sum()
            distrib = np.random.multinomial(self.dice_number, distrib)
        else:
            distrib = self.distrib
        alpha = self.dice_number / total_dices
        posteriors = self.posteriors * (1.0 - alpha) + distrib * alpha
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

    def update_trust(self, bets, dices, current_state):
        self.posteriors = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0]) / 6.0
