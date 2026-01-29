// --- State ---
let board = ['', '', '', '', '', '', '', '', ''];
let currentPlayer = 'X';
let gameOver = false;
let mode = 'pvp';

const WIN_LINES = [
  [0, 1, 2], [3, 4, 5], [6, 7, 8],
  [0, 3, 6], [1, 4, 7], [2, 5, 8],
  [0, 4, 8], [2, 4, 6]
];

const boardEl = document.getElementById('board');
const statusEl = document.getElementById('status');
const modeEl = document.getElementById('mode');
const resetEl = document.getElementById('reset');

function getWinner() {
  for (const [a, b, c] of WIN_LINES) {
    if (board[a] && board[a] === board[b] && board[b] === board[c]) return board[a];
  }
  return null;
}

function isDraw() {
  return !getWinner() && board.every(cell => cell !== '');
}

function updateStatus() {
  const winner = getWinner();
  if (winner) {
    statusEl.textContent = `${winner} wins!`;
    return;
  }
  if (isDraw()) {
    statusEl.textContent = "It's a draw!";
    return;
  }
  statusEl.textContent = `${currentPlayer}'s turn`;
}

function renderBoard() {
  boardEl.querySelectorAll('button').forEach((btn, i) => {
    btn.textContent = board[i] || '';
    btn.disabled = gameOver || board[i] !== '';
    btn.dataset.value = board[i] || '';
  });
}

function emptyIndices() {
  return board.map((v, i) => (v === '' ? i : -1)).filter(i => i >= 0);
}

function aiMoveEasy() {
  const indices = emptyIndices();
  return indices[Math.floor(Math.random() * indices.length)];
}

function aiMoveMedium() {
  const ai = 'O', human = 'X';
  for (const [a, b, c] of WIN_LINES) {
    const line = [board[a], board[b], board[c]];
    const count = p => line.filter(v => v === p).length;
    if (count(ai) === 2 && count('') === 1) {
      if (board[a] === '') return a;
      if (board[b] === '') return b;
      if (board[c] === '') return c;
    }
  }
  for (const [a, b, c] of WIN_LINES) {
    const line = [board[a], board[b], board[c]];
    const count = p => line.filter(v => v === p).length;
    if (count(human) === 2 && count('') === 1) {
      if (board[a] === '') return a;
      if (board[b] === '') return b;
      if (board[c] === '') return c;
    }
  }
  return aiMoveEasy();
}

function getAIMove() {
  if (mode === 'easy') return aiMoveEasy();
  if (mode === 'medium') return aiMoveMedium();
  return -1;
}

function makeMove(index) {
  if (gameOver || board[index] !== '') return;
  board[index] = currentPlayer;
  const winner = getWinner();
  const draw = isDraw();
  if (winner || draw) {
    gameOver = true;
    updateStatus();
    renderBoard();
    return;
  }
  currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
  updateStatus();
  renderBoard();
  if (!gameOver && (mode === 'easy' || mode === 'medium') && currentPlayer === 'O') {
    setTimeout(() => {
      const aiIndex = getAIMove();
      if (aiIndex >= 0) makeMove(aiIndex);
    }, 400);
  }
}

function reset() {
  board = ['', '', '', '', '', '', '', '', ''];
  currentPlayer = 'X';
  gameOver = false;
  mode = modeEl.value;
  updateStatus();
  renderBoard();
}

function init() {
  boardEl.innerHTML = '';
  for (let i = 0; i < 9; i++) {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.dataset.index = String(i);
    btn.setAttribute('aria-label', `Cell ${i + 1}`);
    btn.addEventListener('click', () => makeMove(i));
    boardEl.appendChild(btn);
  }
  modeEl.addEventListener('change', () => { mode = modeEl.value; });
  resetEl.addEventListener('click', reset);
  updateStatus();
  renderBoard();
}

init();
