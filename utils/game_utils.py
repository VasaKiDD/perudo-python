import random


def player_starting(players_names):
    """
    Simulate a dice roll for every player and return the name of the player who reached the higher score first.
    :param players_names: list of the players' names.
    :return starting_player: name of the player that starts.
    """
    starting_player = 0
    val_starting_player = 0
    for name in players_names:
        val_player = random.sample([1, 2, 3, 4, 5, 6], 1)
        if val_player > val_starting_player:
            val_starting_player = val_player
            starting_player = name
    return starting_player


def get_players_names(nb_player):
    """
    Pick random names for the players in a pre-defined list of names.
    :param nb_player: number of players in need of a name.
    :return
    """
    name_list = ["Bobby", "Johny", "Suzan", "Karen", "Lauren", "Anthony", "David", "Isa", "Matthew", "Pablo", "Sofia"]
    if nb_player > len(name_list):
        print("To many players not enough names, please choose a number of "
              "players inferior to {} or add new names in the name_list of the function"
              "'get_players_names' in the file 'utils/game_utils.py".format(len(name_list)))
    player_name = random.sample(name_list, nb_player)
    return player_name
