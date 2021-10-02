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

    def bet_validity(self):
        self.current_bet = 1

    def play_round(self):
        self.current_bet = 1

    def play_game(self):
        self.current_bet = 1


game = PerudoGame(4)
game.players_initialization()

