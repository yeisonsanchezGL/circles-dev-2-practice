const WIN_LINES = [
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8],
  [0, 3, 6],
  [1, 4, 7],
  [2, 5, 8],
  [0, 4, 8],
  [2, 4, 6],
];

const board = document.getElementById("board");
const turnEl = document.getElementById("turn");
const resetBtn = document.getElementById("reset");
const winsXEl = document.getElementById("wins-x");
const winsOEl = document.getElementById("wins-o");
const drawsEl = document.getElementById("draws");

let state = [];
let currentPlayer = "X";
let gameOver = false;
let scores = { X: 0, O: 0, draw: 0 };

function init() {
  state = Array(9).fill(null);
  currentPlayer = "X";
  gameOver = false;
  updateTurnDisplay();
  board.querySelectorAll(".cell").forEach((cell, i) => {
    cell.textContent = "";
    cell.className = "cell";
    cell.disabled = false;
  });
}

function updateTurnDisplay(message) {
  if (message !== undefined) {
    turnEl.textContent = message;
    turnEl.className = "turn-indicator " + (message.includes("X") ? "win-x" : message.includes("O") ? "win-o" : "draw");
    return;
  }
  turnEl.textContent = `Player ${currentPlayer}'s turn`;
  turnEl.className = "turn-indicator";
}

function checkWinner() {
  for (const [a, b, c] of WIN_LINES) {
    if (state[a] && state[a] === state[b] && state[a] === state[c]) {
      return { winner: state[a], line: [a, b, c] };
    }
  }
  return null;
}

function checkDraw() {
  return state.every((cell) => cell !== null);
}

function highlightWinningCells(line) {
  line.forEach((i) => {
    const cell = board.querySelector(`[data-index="${i}"]`);
    if (cell) cell.classList.add("winning");
  });
}

function endGame(result) {
  gameOver = true;
  board.querySelectorAll(".cell").forEach((c) => (c.disabled = true));

  if (result.winner) {
    scores[result.winner]++;
    if (result.winner === "X") winsXEl.textContent = scores.X;
    else winsOEl.textContent = scores.O;
    highlightWinningCells(result.line);
    updateTurnDisplay(`Player ${result.winner} wins!`);
  } else {
    scores.draw++;
    drawsEl.textContent = scores.draw;
    updateTurnDisplay("It's a draw!");
  }
}

function makeMove(index) {
  if (gameOver || state[index] !== null) return;

  state[index] = currentPlayer;
  const cell = board.querySelector(`[data-index="${index}"]`);
  cell.textContent = currentPlayer;
  cell.classList.add(currentPlayer.toLowerCase());
  cell.disabled = true;

  const result = checkWinner();
  if (result) {
    endGame(result);
    return;
  }
  if (checkDraw()) {
    endGame({});
    return;
  }

  currentPlayer = currentPlayer === "X" ? "O" : "X";
  updateTurnDisplay();
}

board.addEventListener("click", (e) => {
  const cell = e.target.closest(".cell");
  if (cell) makeMove(Number(cell.dataset.index));
});

resetBtn.addEventListener("click", init);

init();
