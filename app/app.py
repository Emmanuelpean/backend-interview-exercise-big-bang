# Asked: Interactive Gameplay: Players can select their choice, and the winner is determined based on the rules.
# Implemented: Possible improvement: adding a selection cursor for the choices instead of typing

# Asked: Clear Visual Feedback: Winning and losing outcomes are displayed in an engaging and intuitive way.
# Implement. Possible improvement: Adding colored feedback using a Logger object

# Scoreboard: Tracks the points of the user and the computer across multiple rounds.
# Implemented

# Data Persistence: Retains the game state and scoreboard.
# To implement by storing data into a json. In this case, ask user if they want to continue a game, or start a new one

# Restart: Allows the user to restart the game, clearing the scoreboard and resetting the game state.

# Start time: 14:44

from typing import Literal, get_args

# List of choices for both players
choices = Literal['rock', 'paper', 'scissors', 'lizard', 'spock']  # Literal adds value check and auto-completion in IDE
choices_list = list(get_args(choices))

# Dictionary to keep track of the score
score = {'Player 1': 0, 'Player 2': 0}

# Defines a dictionary that maps each choice (key) to a list of tuples.
# Each tuple contains a choice that it defeats and the verb describing how it wins.
win_dict = {'scissors': [('paper', 'cut'), ('lizard', 'decapitates')],
            'paper': [('rock', 'covers'), ('spock', 'disproves')],
            'rock': [('scissors', 'crushes'), ('lizard', 'crushes')],
            'lizard': [('paper', 'eats'), ('spock', 'poisons')],
            'spock': [('scissors', 'smashes'), ('rock', 'vaporizes')]}


def get_player_choice(player_name: str) -> str:
    """ Get the player choice
    :param str player_name: player name
    :return: the player choice or raise an exception if the choice is not in the list """

    choice = input(f'{player_name}: Please choose an option in {choices_list}').strip().lower()
    if choice not in choices_list + ['quit']:
        raise Exception('Please choose something in the list')
    return choice


def display_score(adjective: str = '') -> None:
    """ Print the score in the console
    :param str adjective: optional string characterising the score """

    print(f"\nThe {adjective} score is\n"
          f"Player 1: {score['Player 1']}\n"
          f"Player 2: {score['Player 2']}\n")


def get_playera_score(choice_A: str, choice_B: str, player_A: str, player_B: str) -> int:
    """Determine if choice_A beats choice_B based on win_dict.
    :param str choice_A: choice A
    :param str choice_B: choice B
    :param str player_A: player name associated with choice A
    :param str player_B: player name associated with choice B
    :return: 1 victory point if choice A beats choice B, else 0 """

    wins_against_tuple = win_dict[choice_A]  # list of tuples which choice A beats
    wins_against_choices = [tup[0] for tup in wins_against_tuple]  # list of choices which choice A beats
    try:
        verb_index = wins_against_choices.index(choice_B)
        verb = wins_against_tuple[verb_index][1]
        print(f"\n\n{player_A} has selected {choice_A} while {player_B} selected {choice_B}.\n"
              f"{choice_A.capitalize()} {verb} {choice_B}\n"
              f"{player_A} wins this round!!!")
        return 1
    except ValueError:
        return 0


def play():
    while True:

        # Get the player choices
        player1_choice = get_player_choice('Player 1')
        player2_choice = get_player_choice('Player 2')
        if player1_choice == 'quit' or player2_choice == 'quit':
            print('One of the players has decided to quit the game. Game ending. Thanks for playing.')
            display_score('final')
            if score['Player 1'] > score['Player 2']:
                print('Player 1 wins the game!!!')
            elif score['Player 1'] < score['Player 2']:
                print('Player 2 wins the game!!!')
            else:
                print("It's a tie")
            break

        # Determine who won
        if player1_choice == player2_choice:
            print(f"Both players selection {player1_choice}. It's a tie!!!")
        score['Player 1'] += get_playera_score(player1_choice, player2_choice, 'Player 1', 'Player 2')
        score['Player 2'] += get_playera_score(player2_choice, player1_choice, 'Player 2', 'Player 1')

        display_score('current')


if __name__ == "__main__":
    play()
