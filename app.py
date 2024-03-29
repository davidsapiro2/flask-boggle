from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}
print("**********************games cleared**********************************")

@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start new game and return JSON about game.

    Returns: JSON of {
       gameId: "...uuid-of-game...",
       board: [ [ 'A', 'B', ... ], ... ]
    }
    """

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    game_info = {
        "gameId": game_id,
        "board": game.board
    }

    return jsonify(game_info)

@app.post("/api/score-word")
def score_word():
    """Gets game id and word, check if the word is on the board and in
    the dictionary. Returns a jsonify answer according to the word's
    existence on the board or in the dictionary."""

    game_id = request.json['gameId']
    word = request.json['word']
    game = games[game_id]

    if not game.word_list.check_word(word):
        return jsonify({"result": "not-word"})

    if not game.check_word_on_board(word):
        return jsonify({"result": "not-on-board"})

    return jsonify({"result": "ok"})
