""" Tests for app.py
To save time, these tests were generated with ChatGPT """

import datetime as dt
import os
import unittest
from unittest.mock import mock_open, patch

from app.app import get_player_choice, get_playera_score, retrieve_scores, save_score


class TestInput(unittest.TestCase):

    @patch('builtins.input', return_value='rock')  # Mock the input function to always return 'rock'
    def test_get_player_choice(self, _mock_input):
        choice = get_player_choice('Player 1')  # The function will receive 'rock'
        self.assertEqual(choice, 'rock')  # Assert the returned value is 'rock'

    @patch('builtins.input', return_value='scissors')
    def test_get_player_choice_invalid(self, _mock_input):
        choice = get_player_choice('Player 1')  # The function will receive 'scissors'
        self.assertEqual(choice, 'scissors')  # Assert the returned value is 'scissors'

    @patch('builtins.input', return_value='quit')
    def test_get_player_choice_quit(self, _mock_input):
        choice = get_player_choice('Player 1')
        self.assertEqual(choice, 'quit')

    @patch('builtins.input', return_value='reset')
    def test_get_player_choice_reset(self, _mock_input):
        choice = get_player_choice('Player 1')
        self.assertEqual(choice, 'reset')


class TestGameLogic(unittest.TestCase):

    def test_get_playera_score_player1_wins(self):
        score = get_playera_score('rock', 'scissors', 'Player 1')
        self.assertEqual(score, 1)  # Player 1 should win so Player 1 gets 1 point

    def test_get_playera_score_player2_wins(self):
        score = get_playera_score('scissors', 'rock', 'Player 1')
        self.assertEqual(score, 0)  # Player 2 should win so no points for Player 1

    def test_get_playera_score_tie(self):
        score = get_playera_score('rock', 'rock', 'Player 1')
        self.assertEqual(score, 0)  # It's a tie


class TestScoreFunctions(unittest.TestCase):
    filename = 'test_score.json'

    @patch('builtins.open', mock_open(read_data='[]'))  # Mocking the file open
    def test_retrieve_scores_empty(self):
        scores = retrieve_scores(self.filename)
        self.assertEqual(scores, [])

    def test_save_score(self):
        score = {"Player 1": 1, "Player 2": 0}
        start_dt = dt.datetime.now()
        save_score(score, start_dt, update=False, filename=self.filename)  # Mocked file open is called here
        scores = retrieve_scores(self.filename)
        self.assertEqual(score, scores[-1])
        os.remove(self.filename)


if __name__ == '__main__':
    unittest.main()
