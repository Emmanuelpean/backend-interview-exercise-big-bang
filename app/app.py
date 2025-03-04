# Interactive Gameplay: Players can select their choice, and the winner is determined based on the rules.
# Clear Visual Feedback: Winning and losing outcomes are displayed in an engaging and intuitive way.
# Scoreboard: Tracks the points of the user and the computer across multiple rounds.
# Data Persistence: Retains the game state and scoreboard.
# Restart: Allows the user to restart the game, clearing the scoreboard and resetting the game state.

# Start time: 14:44

from typing import Literal, get_args

choices = Literal['rock', 'paper', 'scissors', 'lizard', 'spock']  # Literal adds value check and auto-completion in IDE
choices_list = get_args(choices)

player1_choice = input(f'Player 1: Please choose in {choices_list}').lower()
if player1_choice not in choices_list:
    raise Exception('Please choose something in the list')

player2_choice = input(f'Player 2: Please choose in {choices_list}').lower()
if player2_choice not in choices_list:
    raise Exception('Please choose something in the list')

# Tie condition
if player1_choice == player2_choice:
    print(f"Both players selection {player1_choice}. It's a tie!!!")

# Defines a dictionary that link a choice (key) with the choices that loses against (values)
logic_dict = {'scissors': ['paper', 'lizard'],
              'paper': ['rock', 'spock'],
              'rock': ['scissors', 'lizard'],
              'lizard': ['paper', 'spock'],
              'spock': ['scissors', 'rock']}

if player2_choice in logic_dict[player1_choice]:
    print(f'Player 1 has selected {player1_choice} while player 2 selection {player2_choice}. Player 1 wins!!!')

elif player1_choice in logic_dict[player2_choice]:
    print(f'Player 1 has selected {player1_choice} while player 2 selection {player2_choice}. Player 2 wins!!!')
