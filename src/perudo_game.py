import random
import time

from src.player import Player
from src.human_player import Human
from utils.game_utils import get_players_names

sleep_time = 0


class PerudoGame:
    def __init__(self, nb_player, no_human=False):
        self.nb_player = nb_player
        self.players = dict()
        self.looser = list()
        self.current_state_play = dict()
        self.start_player = None
        self.rotation = None
        self.d_dices = None
        self.max_bet = None
        self.no_human = no_human

    def update_max_bet(self):
        self.d_dices = {}
        print("The new dice number of each player:")
        for player in self.players.keys():
            self.d_dices[player] = self.players[player].dice_number
            print(
                self.players[player].name,
                ":",
                self.players[player].dice_number,
            )
        time.sleep(sleep_time)
        self.d_dices = {
            player: self.players[player].dice_number
            for player in self.players.keys()
        }
        self.max_bet = "{maxp}d1".format(maxp=sum(self.d_dices.values()))

    def players_initialization(self):
        """
        Generate an instance of the class AiPlayer for the self.nb_player
        players.
        """
        players_names = get_players_names(self.nb_player)
        for name in players_names:
            self.players[name] = Player(name)
        print("Opponents are: {}".format(players_names))

        if not self.no_human:
            human = Human()
            human.get_name(players_names)
            self.players["human"] = human
        self.rotation = list(self.players.keys())
        print("Rolling the dice for the starting player...")
        random.shuffle(self.rotation)
        time.sleep(sleep_time)
        print(self.rotation[0], " starts to speak in the first round !")
        order = "The order is: "
        for player in self.rotation:
            order += self.players[player].name + "->"
        print(order)
        time.sleep(sleep_time)
        self.start_player = self.rotation[0]
        self.update_max_bet()

    def round_roll(self):
        """
        Dice roll for every players.
        """
        print("Everybody roll their dices...")
        time.sleep(sleep_time)
        self.current_state_play = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        for player in self.players.keys():
            self.players[player].player_roll_result()
            for val in self.players[player].current_roll:
                self.current_state_play[val] += 1

    def remove_disqualified(self):
        """
        Check the player list at the end of turn to remove all players with
        "disqualified" status.
        """
        for player in self.players.keys():
            if self.players[player].player_status == "disqualified":
                if player == "human":
                    return True
                del self.players[player]
                if self.start_player == player:
                    ix = self.rotation.index(player)
                    if ix < len(self.rotation) - 1:
                        self.start_player = self.rotation[ix + 1]
                    else:
                        self.start_player = self.rotation[0]
                self.rotation.remove(player)
                self.nb_player -= 1
                if self.nb_player == 0:
                    return True
                break

        order = "The order is: "
        for player in self.rotation:
            order += self.players[player].name + "->"
        print(order)
        self.update_max_bet()
        return False

    def bet_values_check(self, bet_dice_nb, bet_dice_val):
        """
        Check the validiy of one bet alone.
        """
        max_dice = sum(self.d_dices.values())
        if bet_dice_val == 1:
            if bet_dice_nb > max_dice:
                print(
                    "BetError: You bet more dices than possible dices. "
                    "Do the Math !"
                )
                return False
        else:
            if bet_dice_nb > 2 * max_dice:
                print(
                    "BetError: You bet more dices than possible dices. "
                    "Do the Math !"
                )
                return False

        return True

    def bet_validity(self, new_bet, current_bet):
        """
        Check all the rules for the perudo game betting system by confronting
        new_bet with current bet
        """
        new_bet_dice_nb, new_bet_dice_val = [
            int(val) for val in new_bet.split("d")
        ]
        if not self.bet_values_check(new_bet_dice_nb, new_bet_dice_val):
            return False

        if current_bet is not None:
            cur_bet_dice_nb, cur_bet_dice_val = [
                int(val) for val in current_bet.split("d")
            ]

            if cur_bet_dice_val == 1:
                if new_bet_dice_val == 1:
                    if not new_bet_dice_nb > cur_bet_dice_nb:
                        print(
                            "BetError: You put less pacos dices than current "
                            "paco dices"
                        )
                        return False
                    else:
                        return True
                else:
                    if not new_bet_dice_nb >= cur_bet_dice_nb * 2 + 1:
                        print(
                            "BetError: You put less dices than 2 times the "
                            "non paco value"
                        )
                        return False
                    else:
                        return True
            else:
                if new_bet_dice_val == 1:
                    if not new_bet_dice_nb >= cur_bet_dice_nb // 2 + 1:
                        print(
                            "BetError: You put less dices than 2 times the "
                            "half of current value"
                        )
                        return False
                    else:
                        return True
                else:
                    if not (
                        (new_bet_dice_nb > cur_bet_dice_nb)
                        or (new_bet_dice_val > cur_bet_dice_val)
                    ):
                        print(
                            "BetError: You put less or equal dices than "
                            "current amount of dices",
                            " or a less or equal not paco number",
                        )
                        return False
                    else:
                        return True

        return True

    def dudo(self, current_bet, current_player, last_player):
        """
        This is a function when current player calls dudo on last player. It
        will check who wins the dudo and update dices.
        """

        print("Let's reveal the dices :", self.current_state_play)
        time.sleep(sleep_time)

        # print(self.current_state_play)
        cur_bet_values = current_bet.split("d")
        cur_bet_dice_nb = int(cur_bet_values[0])
        cur_bet_dice_val = int(cur_bet_values[1])
        if cur_bet_dice_val == 1:
            if cur_bet_dice_nb >= self.current_state_play[1]:
                self.players[self.rotation[last_player]].player_fails()
                self.start_player = self.rotation[current_player]
            else:
                self.players[self.rotation[current_player]].player_fails()
                self.start_player = self.rotation[last_player]
        else:
            if (
                cur_bet_dice_nb
                >= self.current_state_play[1]
                + self.current_state_play[cur_bet_dice_val]
            ):
                self.players[self.rotation[last_player]].player_fails()
                self.start_player = self.rotation[current_player]
            else:
                self.players[self.rotation[current_player]].player_fails()
                self.start_player = self.rotation[last_player]
        time.sleep(sleep_time)

    def calza(self, current_bet, current_player):
        """
        This is a function when current player calls calza. It
        will check if he wins the calza and update his dices
        """
        # print(self.current_state_play)
        cur_bet_values = current_bet.split("d")
        cur_bet_dice_nb = int(cur_bet_values[0])
        cur_bet_dice_val = int(cur_bet_values[1])

        print("Let's reveal the dices :", self.current_state_play)
        time.sleep(sleep_time)

        if (
            self.current_state_play[cur_bet_dice_val]
            <= cur_bet_dice_nb
            <= self.current_state_play[1]
            + self.current_state_play[cur_bet_dice_val]
        ):
            self.players[self.rotation[current_player]].player_wins_calza()
            self.start_player = self.rotation[current_player]
        else:
            self.players[self.rotation[current_player]].player_fails()
            self.start_player = self.rotation[current_player]
        time.sleep(sleep_time)

    def update_players_trust(self, bet_history):
        player_dices = []
        for name, player_instance in self.players.items():
            player_dices.append((name, player_instance.current_roll))
        for player_instance in self.players.values():
            player_instance.update_trust(
                bet_history, player_dices, self.current_state_play
            )

    def play_round(self):
        """
        Function handling one round of a play
        """
        self.round_roll()
        current_bet = None
        bet_history = []
        last_player = 0
        current_player = self.rotation.index(self.start_player)
        end_round = False
        while not end_round:
            action, new_bet = self.players[
                self.rotation[current_player]
            ].make_choice(bet_history, self.d_dices)
            if action == "accept":
                while not self.bet_validity(new_bet, current_bet):
                    action, new_bet = self.players[
                        self.rotation[current_player]
                    ].make_choice(bet_history, self.d_dices)
                print(
                    "{p} accepts and bets {n} dices of value {v}".format(
                        p=self.players[self.rotation[current_player]].name,
                        n=new_bet.split("d")[0],
                        v=new_bet.split("d")[1],
                    )
                )
                time.sleep(sleep_time)
                bet_history.append((self.rotation[current_player], new_bet))
                last_player = current_player
                current_bet = new_bet
                current_player = (
                    current_player + 1
                    if current_player < len(self.rotation) - 1
                    else 0
                )
                if current_bet == self.max_bet:
                    print(
                        "{p} calls dudo".format(
                            p=self.rotation[current_player]
                        )
                    )
                    time.sleep(sleep_time)
                    self.dudo(current_bet, current_player, last_player)
                    end_round = True
            elif action == "dudo":
                print(
                    "{p} calls dudo".format(
                        p=self.players[self.rotation[current_player]].name
                    )
                )
                time.sleep(sleep_time)
                self.dudo(current_bet, current_player, last_player)
                end_round = True
            elif action == "calza":
                print(
                    "{p} calls calza".format(
                        p=self.players[self.rotation[current_player]].name
                    )
                )
                time.sleep(sleep_time)
                self.calza(current_bet, current_player)
                end_round = True
            else:
                print("!!!! Action Error !!!!")
        self.update_players_trust(bet_history)

    def play_game(self):
        """
        Function handling one play of the game between players
        """
        self.players_initialization()
        game_end = False
        while not game_end:
            self.play_round()
            game_end = self.remove_disqualified()

        if self.nb_player == 0:
            if self.no_human:
                print("Last Player Wins")
            else:
                print("Congrats, you won !")
