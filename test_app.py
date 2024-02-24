from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            ...

            self.assertEqual(response.status_code, 200)
            self.assertIn('<title>Boggle</title>', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with app.test_client() as client:

            # make a post request to /api/new-game
            # get the response body as json using .get_json()
            # test that the game_id is a string
            # test that the board is a list
            # test that the game_id is in the dictionary of games (imported from app.py above)
            response = client.post(
                '/api/new-game',

            )
            json_response = response.get_json()
            #check the solution for line 49
            self.assertIsInstance(json_response["gameId"], str)
            self.assertIsInstance(json_response["board"], list)
            self.assertIn(json_response["gameId"], games)

    def test_score_word(self):
        """Test if word is valid"""

        with app.test_client() as client:

            # make a post request to /api/new-game
            # get the response body as json using .get_json()
            # find that game in the dictionary of games (imported from app.py above)

            # manually change the game board's rows so they are not random

            # test to see that a valid word on the altered board returns {'result': 'ok'}
            # test to see that a valid word not on the altered board returns {'result': 'not-on-board'}
            # test to see that an invalid word returns {'result': 'not-word'}

            new_game_response = client.post(
                '/api/new-game'
            )
            json_new_game_response = new_game_response.get_json()


            current_game = games[json_new_game_response["gameId"]]
            current_game.board =[
                ["H", "E", "L", "L", "O"],
                ["D", "A", "V", "I", "D"],
                ["D", "A", "V", "I", "D"],
                ["D", "A", "V", "I", "D"],
                ["D", "A", "V", "I", "D"]
            ]

            score_invalid_word_response = client.post(
                'api/score-word',
                json= {
                    "gameId": json_new_game_response["gameId"],
                    "word": "DAVID",
                }
            )

            json_score_invalid_word_response = score_invalid_word_response.get_json()

            self.assertEqual(json_score_invalid_word_response["result"], "not-word")

            score_valid_word_response = client.post(
                'api/score-word',
                json= {
                    "gameId": json_new_game_response["gameId"],
                    "word": "HELLO",
                }
            )

            json_score_valid_word_response = score_valid_word_response.get_json()

            self.assertEqual(json_score_valid_word_response["result"], "ok")

            score_not_on_board_word_response = client.post(
                'api/score-word',
                json= {
                    "gameId": json_new_game_response["gameId"],
                    "word": "HOUSE",
                }
            )

            json_score_not_on_board_word_response = score_not_on_board_word_response.get_json()

            self.assertEqual(json_score_not_on_board_word_response["result"], "not-on-board")


