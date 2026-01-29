const boardEl = document.getElementById('board');
const statusEl = document.getElementById('status');
const resetBtn = document.getElementById('reset');

let board = ['', '', '', '', '', '', '', '', ''];
let currentPlayer = 'X';
let gameOver = false;

const LINES = [
  [0, 1, 2], [3, 4, 5], [6, 7, 8],
  [0, 3, 6], [1, 4, 7], [2, 5, 8],
  [0, 4, 8], [2, 4, 6]
];

function checkWinner() {
  for (const [a, b, c] of LINES) {
    if (board[a] && board[a] === board[b] && board[b] === board[c]) {
      return board[a];
    }
  }
  if (board.every(cell => cell !== '')) return 'draw';
  return null;
}

function makeMove(index) {
  if (gameOver || board[index] !== '') return;
  board[index] = currentPlayer;
  const cell = boardEl.children[index];
  cell.textContent = currentPlayer;
  cell.classList.add('taken', currentPlayer.toLowerCase());

  const winner = checkWinner();
  if (winner === 'draw') {
    statusEl.textContent = "It's a draw!";
    gameOver = true;
  } else if (winner) {
    statusEl.textContent = `Player ${winner} wins!`;
    gameOver = true;
  } else {
    currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
    statusEl.textContent = `Player ${currentPlayer}'s turn`;
  }
}

function reset() {
  board = ['', '', '', '', '', '', '', '', ''];
  currentPlayer = 'X';
  gameOver = false;
  statusEl.textContent = "Player X's turn";
  Array.from(boardEl.children).forEach(cell => {
    cell.textContent = '';
    cell.classList.remove('taken', 'x', 'o');
  });
}

boardEl.addEventListener('click', (e) => {
  const cell = e.target.closest('.cell');
  if (cell) makeMove(Number(cell.dataset.index));
});
resetBtn.addEventListener('click', reset);
