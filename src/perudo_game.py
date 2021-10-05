from ai_player import AiPlayer
from human_player import Human
from utils.game_utils import player_starting, get_players_names


class PerudoGame:
    def __init__(self, nb_player):
        self.nb_player = nb_player
        self.players = dict()
        self.looser = list()
        self.current_state_play = dict()
        self.current_bet = "0d0"

    def players_initialization(self):
        """
        Generate an instance of the class AiPlayer for the self.nb_player players.
        """
        players_names = get_players_names(self.nb_player)
        for name in players_names:
            self.players[name] = AiPlayer(name)
        print("Your opponents are: {}".format(players_names))
        self.players["human"] = Human().get_name(players_names)

    def round_roll(self):
        """
        Dice roll for every players.
        """
        self.current_state_play = {1: 0,
                                   2: 0,
                                   3: 0,
                                   4: 0,
                                   5: 0,
                                   6: 0}
        for player_name in self.players.keys():
            if player_name == 'human':
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
                del self.players[player]

    def bet_validity(self, new_bet):
        if not isinstance(new_bet, str):
            print("Your bet should be a string.")
        # TODO: add a regex that check if the bet follow the style "{int}d{int}"
        new_bet_values = new_bet.split("d")
        new_bet_dice_nb = int(new_bet_values[0])
        new_bet_dice_val = int(new_bet_values[1])

        cur_bet_values = self.current_bet.split("d")
        cur_bet_dice_nb = int(cur_bet_values[0])
        cur_bet_dice_val = int(cur_bet_values[1])
        valid_bet = True
        if new_bet_dice_nb < cur_bet_dice_nb:
            if new_bet_dice_val == 1:
                if new_bet_dice_nb >= cur_bet_dice_nb//2:
                    valid_bet = False
                    print("if you want to bet on 1 the number of dice should at least be more"
                          " than half the current number of dices.")
            else:
                valid_bet = False
                print("if you want to bet then put more dices or a bigger value.")
        elif new_bet_dice_nb == cur_bet_dice_nb:
            if cur_bet_dice_val >= new_bet_dice_val:
                valid_bet = False
                print("if you want to bet then put more dices or a bigger value.")
        else:
            pass

        if valid_bet:
            self.current_bet = new_bet

    def play_round(self):
        self.current_bet = 1

    def play_game(self):
        self.current_bet = 1


game = PerudoGame(4)
game.players_initialization()

