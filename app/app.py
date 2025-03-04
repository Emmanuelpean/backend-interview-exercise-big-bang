""" This script (and the additional test.py) was written in ~3h for Automata.
The requirements for this script were as below:
* Requirement: Interactive Gameplay: Players can select their choice, and the winner is determined based on the rules.
* Requirement: Clear Visual Feedback: Winning and losing outcomes are displayed in an engaging and intuitive way.
* Requirement: Scoreboard: Tracks the points of the user and the computer across multiple rounds.
* Requirement: Data Persistence: Retains the game state and scoreboard.
* Requirement: Restart: Allows the user to restart the game, clearing the scoreboard and resetting the game state.

I believed that I have met all the requirements below. If I had had more time, I would have
* added a selection cursor for the choices instead of typing
* added colored feedback using a Logger object
* increased the test coverage

Notes: I decided to go for a function orientated approach here as the code is relatively simple. if the code were
to become any more complex, I would consider moving to OOP to make the code more readable. """

import datetime as dt
import json
from typing import Tuple

__version__ = '0.4.0'

# ----------------------------------------------------- SCORE FILE -----------------------------------------------------

SCORE_FILENAME = 'scores.json'


def retrieve_scores(filename: str = SCORE_FILENAME) -> list:
    """ Return the scores from the json file
    :param str filename: filename """

    try:
        with open(filename, "r") as file:
            return json.load(file)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        return []


def save_score(score: dict, start_dt: dt.datetime, update: bool, filename: str = SCORE_FILENAME) -> None:
    """Append the score to the json score file
    :param dict score: current score to store
    :param dt.datetime start_dt: game start date and time
    :param bool update: if True, update the last score in the file, else appends to it
    :param str filename: filename"""

    # Load the previous scores
    scores = retrieve_scores(filename)

    # Add the datetimes to the score and either replace the last score or append it to the list
    score.update({"Last Played On": dt.datetime.now().isoformat()})
    if update:
        score.update({"Started On": scores[-1]["Started On"]})
        scores[-1] = score
    else:
        score.update({"Started On": start_dt.isoformat()})
        scores.append(score)

    # Save the new score
    with open(filename, "w") as file:
        # noinspection PyTypeChecker
        json.dump(scores, file, indent=4)


# ----------------------------------------------------- GAME LOGIC -----------------------------------------------------


# List of choices for both players
CHOICES = ['rock', 'paper', 'scissors', 'lizard', 'spock']

# Defines a dictionary that maps each choice (key) to a list of tuples.
# Each tuple contains a choice that it defeats and the verb describing how it wins.
LOGIC_DICT = {"scissors": [("paper", "cut"), ("lizard", "decapitates")],
              "paper": [("rock", "covers"), ("spock", "disproves")],
              "rock": [("scissors", "crushes"), ("lizard", "crushes")],
              "lizard": [("paper", "eats"), ("spock", "poisons")],
              "spock": [("scissors", "smashes"), ("rock", "vaporizes")]}


def get_player_choice(player_name: str) -> str:
    """ Get the player choice
    :param str player_name: player name
    :return: the player choice or raise an exception if the choice is not in the list """

    while True:
        choice = input(f"{player_name}: Please choose an option in ({', '.join(CHOICES)})"
                       f", type 'quit' to quit the game, or type 'reset' to reset the current game.").strip().lower()
        if choice in CHOICES + ["quit", "reset"]:
            break
        else:
            print('Choice is not in the list. Please try again.')
    return choice


def display_score(score: dict, adjective: str) -> None:
    """ Print the score in the console
    :param dict score: score dictionary containing values for Player 1 and Player 2
    :param str adjective: optional string characterising the score """

    print(f"\nThe {adjective} score is\n"
          f"Player 1: {score['Player 1']}\n"
          f"Player 2: {score['Player 2']}\n")


def get_playera_score(choice_A: str, choice_B: str, player_A: str) -> int:
    """ Determine if choice_A beats choice_B based on logic_dict.
    :param str choice_A: choice A
    :param str choice_B: choice B
    :param str player_A: player name associated with choice A
    :return: 1 victory point if choice A beats choice B, else 0 """

    wins_against_tuple = LOGIC_DICT[choice_A]  # list of tuples which choice A beats
    wins_against_choices = [tup[0] for tup in wins_against_tuple]  # list of choices which choice A beats
    try:
        verb_index = wins_against_choices.index(choice_B)
        verb = wins_against_tuple[verb_index][1]
        print(f"{choice_A.capitalize()} {verb} {choice_B.capitalize()}. {player_A} wins this round!!!")
        return 1
    except ValueError:
        return 0


# --------------------------------------------------- GAME FUNCTIONS ---------------------------------------------------


def exit_game(player: str, score: dict, start_dt: dt.datetime, replace: bool) -> None:
    """ Exit the game by displaying the final score and saving it to the json file
    :param player: name of the player who decided to end the game
    :param score: score dictionary
    :param start_dt: game start datetime
    :param replace: if True, replace the last score, else append """

    print(f"{player} has decided to quit the game. Game ending. Thanks for playing.")

    # Display the final score and which player won
    display_score(score, "final")
    if score["Player 1"] > score["Player 2"]:
        print("Player 1 wins the game!!!")
    elif score["Player 1"] < score["Player 2"]:
        print("Player 2 wins the game!!!")
    else:
        print("It's a tie!")

    # Save the score to the json score file
    save_score(score, start_dt, replace)


def start_game() -> Tuple[dict, dt.datetime]:
    """ Start the game by setting the score to its initial values and capture the start datetime """
    current_score = {'Player 1': 0, 'Player 2': 0}
    start_dt = dt.datetime.now()
    return current_score, start_dt


def reset_game() -> Tuple[dict, dt.datetime]:
    """ Reset the current game state """
    print('Resetting the current score and game start datetime')
    return start_game()


def play() -> None:
    current_score, start_dt = start_game()  # set the new start score and datetime
    update_score = False  # determines if the last score is replaced or not
    scores = retrieve_scores()  # previous scores

    if scores:

        # Ask if the player wants to check previous scores
        while True:
            check_scores = input("Do you want to check previous scores? (Y/N) ").strip().lower()
            if check_scores == "y":
                print("\nPrevious scores:")
                for score in scores:
                    print(f"Started on: {score['Started On']} | Player 1: {score['Player 1']} | "
                          f"Player 2: {score['Player 2']}")
                break
            elif check_scores == "n":
                break
            else:
                print("Invalid input. Please try again.")

        # Check if the players want to continue the previous games
        while True:
            question = input("Do you want to resume your previous game? (Y/N)").strip().lower()
            if question == "y":
                current_score = scores[-1]
                update_score = True
                break
            elif question == "n":
                break
            else:
                print("Invalid input. Please try again.")

    while True:

        # Get player 1 choice
        player1_choice = get_player_choice("Player 1")
        if player1_choice == "quit":
            exit_game("Player 1", current_score, start_dt, update_score)
            break
        if player1_choice == "reset":
            current_score, start_dt = reset_game()
            continue

        # Get player 2 choice
        player2_choice = get_player_choice("Player 2")
        if player2_choice == "quit":
            exit_game("Player 2", current_score, start_dt, update_score)
            break
        if player1_choice == "reset":
            current_score, start_dt = reset_game()
            continue

        # Determine who won
        print(
            f"\nPlayer 1 selected {player1_choice.capitalize()} while Player 2 selected {player2_choice.capitalize()}.")
        if player1_choice == player2_choice:
            print("It's a tie!!!")
        current_score['Player 1'] += get_playera_score(player1_choice, player2_choice, "Player 1")
        current_score['Player 2'] += get_playera_score(player2_choice, player1_choice, "Player 2")

        display_score(current_score, "current")


if __name__ == "__main__":
    play()
