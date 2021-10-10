import re
import random

from src.ai_player import AiPlayer
from src.human_player import Human
from utils.game_utils import player_starting, get_players_names


class PerudoGame:
    def __init__(self, nb_player):
        self.nb_player = nb_player
        self.players = dict()
        self.looser = list()
        self.current_state_play = dict()
        self.start_player = None
        self.rotation = None
        self.d_dices = None
        self.max_bet = None

    def update_max_bet(self):
        self.d_dices = {}
        print("The new dice number for each player is :")
        for player in self.players.keys():
            self.d_dices[player] = self.players[player].dice_number
            print(
                self.players[player].name,
                ":",
                self.players[player].dice_number,
            )
        self.d_dices = {
            player: self.players[player].dice_number
            for player in self.players.keys()
        }
        self.max_bet = "{maxp}d1".format(
            maxp=(self.nb_player + 1) * sum(self.d_dices.values())
        )

    def players_initialization(self):
        """
        Generate an instance of the class AiPlayer for the self.nb_player players.
        """
        players_names = get_players_names(self.nb_player)
        for name in players_names:
            self.players[name] = AiPlayer(name)
        print("Your opponents are: {}".format(players_names))
        human = Human()
        human.get_name(players_names)
        self.players["human"] = human
        self.rotation = list(self.players.keys())
        random.shuffle(self.rotation)
        self.update_max_bet()

    def round_roll(self):
        """
        Dice roll for every players.
        """
        self.current_state_play = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        for player_name in self.players.keys():
            if player_name == "human":
                self.players["human"].get_human_roll()
                for val in self.players["human"].current_roll:
                    self.current_state_play[val] += 1
            else:
                self.players[player_name].player_roll_result()
                for val in self.players["human"].current_roll:
                    self.current_state_play[val] += 1

    def remove_disqualified(self):
        """
        Check the player list at the end of turn to remove all players with "disqualified" status.
        """
        for player in self.players.keys():
            if self.players[player].status == "disqualified":
                if player == "human":
                    return True
                print("AI Player {p} is disqualified !".format(p=player))
                del self.players[player]
                self.nb_player -= 1
        self.rotation = list(self.players.keys())
        random.shuffle(self.rotation)
        self.update_max_bet()
        return False

    def bet_validity(self, current_bet, new_bet):
        assert isinstance(new_bet, str), "Your bet should be a string."
        new_bet = re.match("([0-9]+)d([0-9]+)", new_bet)
        assert new_bet is not None, "Invalid bet, should be {int}d{int}"
        new_bet_values = new_bet.groups()
        new_bet_dice_nb = int(new_bet_values[0])
        new_bet_dice_val = int(new_bet_values[1])

        cur_bet_values = current_bet.split("d")
        cur_bet_dice_nb = int(cur_bet_values[0])
        cur_bet_dice_val = int(cur_bet_values[1])
        valid_bet = True
        if new_bet_dice_nb < cur_bet_dice_nb:
            if new_bet_dice_val == 1:
                if new_bet_dice_nb >= cur_bet_dice_nb // 2:
                    valid_bet = False
                    print(
                        "if you want to bet on 1 the number of dice should at least be more"
                        " than half the current number of dices."
                    )
            else:
                valid_bet = False
                print(
                    "if you want to bet then put more dices or a bigger value."
                )
        elif new_bet_dice_nb == cur_bet_dice_nb:
            if cur_bet_dice_val >= new_bet_dice_val:
                valid_bet = False
                print(
                    "if you want to bet then put more dices or a bigger value."
                )
        else:
            pass

        return valid_bet

    def dudo(self, current_bet, current_player, last_player):
        cur_bet_values = current_bet.split("d")
        cur_bet_dice_nb = int(cur_bet_values[0])
        cur_bet_dice_val = int(cur_bet_values[1])
        if cur_bet_dice_val == 1:
            if cur_bet_dice_nb >= self.current_state_play[1]:
                self.players[self.rotation[last_player]].player_fails()
                self.start_player = current_player
            else:
                self.players[self.rotation[current_player]].player_fails()
                self.start_player = last_player
        else:
            if (
                cur_bet_dice_nb
                >= self.current_state_play[1]
                + self.current_state_play[cur_bet_dice_val]
            ):
                self.players[self.rotation[last_player]].player_fails()
                self.start_player = current_player
            else:
                self.players[self.rotation[current_player]].player_fails()
                self.start_player = last_player

    def calza(self, current_bet, current_player):
        cur_bet_values = current_bet.split("d")
        cur_bet_dice_nb = int(cur_bet_values[0])
        cur_bet_dice_val = int(cur_bet_values[1])
        if (
            cur_bet_dice_nb
            == self.current_state_play[1]
            + self.current_state_play[cur_bet_dice_val]
        ):
            self.players[self.rotation[current_player]].player_wins_calza()
            self.start_player = current_player

    def play_round(self):
        self.round_roll()
        current_bet = None
        last_player = None
        current_player = self.start_player
        end_round = False
        print(self.rotation[self.start_player], " starts.")
        while not end_round:
            action, new_bet = self.players[
                self.rotation[current_player]
            ].make_choice(current_bet, self.rotation[last_player])
            if action == "accept":
                if current_player == "human":
                    valid = False
                    while not valid:
                        action, new_bet = self.players["human"].make_choice(
                            current_bet, self.rotation[last_player]
                        )
                        valid = self.bet_validity(current_bet, new_bet)
                print(
                    "{p} bets {n} dices of value {v}".format(
                        p=self.players[self.rotation[current_player]].name,
                        n=new_bet.split("d")[0],
                        v=new_bet.split("d")[1],
                    )
                )
                last_player = current_player
                current_bet = new_bet
                current_player = (
                    current_player + 1
                    if current_player < len(self.rotation)
                    else 0
                )
                if current_bet == self.max_bet:
                    self.dudo(current_player, last_player)
                    end_round = True
            elif action == "dudo":
                print("{p} calls dudo".format(p=self.rotation[current_player]))
                self.dudo(current_bet, current_player, last_player)
                end_round = True
            elif action == "calza":
                print(
                    "{p} calls calza".format(p=self.rotation[current_player])
                )
                self.calza(current_bet, current_player)
                end_round = True
            else:
                print("!!!! Action Error !!!!")

    def play_game(self):
        self.players_initialization()
        game_end = False
        while not game_end:
            print(
                "The current rotation is {players}".format(
                    players=self.rotation
                )
            )
            self.play_round()
            game_end = self.remove_disqualified()
