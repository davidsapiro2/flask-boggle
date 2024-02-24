"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  const response = await fetch(`/api/new-game`, {
    method: "POST",
  });
  const gameData = await response.json();

  gameId = gameData.gameId;
  let board = gameData.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  $table.empty();
  // loop over board and create the DOM tr/td structure
  for (const row of board) {
    const $row = $("<tr>");
    for (const cell of row) {
      const $cell = $("<td>").text(cell);
      $row.append($cell);
    }
    $table.append($row);
  }
}

/** Grabs entered word from input field */

function getWord() {
  return $wordInput.val();
}

/** Submits entered word to the server and receives response. */

async function submitWord(word) {
  const response = await fetch('/api/score-word', {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      "gameId": gameId,
      "word": word.toUpperCase(),
    })
  });

  const result = await response.json();
  return result;
}


/** Gets the API's response and manipulates the DOM according to that.
 * If the word is not in the dictionary or on the board, it displays a message.
 * Else, it adds the word to correct guesses list.
 */
async function handleResult(response) {
  $message.empty();

  if (response.result === "not-word") {
    $message.append("<p>").text("It is not a word!");
  } else if (response.result === "not-on-board") {
    $message.append("<p>").text("It is not on the board!");
  } else {
    $playedWords.append($("<li>").text($wordInput.val()));
  }
}


async function handleSubmit(evt) {
  evt.preventDefault();
  const word = getWord();
  const wordResponse = await submitWord(word);
  await handleResult(wordResponse);
}

$form.on("submit", handleSubmit);
start();