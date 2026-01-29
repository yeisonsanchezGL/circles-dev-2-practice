(function () {
  'use strict';

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

  let board = ['', '', '', '', '', '', '', '', ''];
  let currentPlayer = 'X';
  let gameOver = false;
  let winningLine = null;

  const statusEl = document.getElementById('status');
  const currentPlayerEl = document.getElementById('current-player');
  const gridEl = document.getElementById('grid');
  const restartBtn = document.getElementById('restart');

  function renderBoard() {
    const cells = gridEl.querySelectorAll('.cell');
    cells.forEach(function (cell, i) {
      const value = board[i];
      cell.textContent = value;
      cell.classList.remove('x', 'o', 'taken', 'winner');
      if (value) {
        cell.classList.add(value.toLowerCase(), 'taken');
      }
    });
    if (winningLine) {
      winningLine.forEach(function (index) {
        gridEl.querySelector('.cell[data-index="' + index + '"]').classList.add('winner');
      });
    }
  }

  function updateStatus() {
    if (gameOver) {
      if (winningLine) {
        statusEl.textContent = 'Winner: ' + currentPlayer + '!';
      } else {
        statusEl.textContent = "It's a draw!";
      }
      currentPlayerEl.textContent = '';
    } else {
      statusEl.textContent = 'Current player: ';
      currentPlayerEl.textContent = currentPlayer;
    }
  }

  /**
   * Returns 'X', 'O', 'draw', or null if game is not over.
   * Sets winningLine (array of 3 indices) when there is a winner.
   */
  function checkWinner() {
    for (var i = 0; i < WIN_LINES.length; i++) {
      var a = WIN_LINES[i][0];
      var b = WIN_LINES[i][1];
      var c = WIN_LINES[i][2];
      if (board[a] && board[a] === board[b] && board[b] === board[c]) {
        winningLine = WIN_LINES[i];
        return board[a];
      }
    }
    winningLine = null;
    if (board.every(Boolean)) {
      return 'draw';
    }
    return null;
  }

  /**
   * Place current player at index. Returns true if move was made.
   */
  function makeMove(index) {
    if (gameOver || board[index]) {
      return false;
    }
    board[index] = currentPlayer;
    var result = checkWinner();
    if (result) {
      gameOver = true;
    } else {
      currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
    }
    renderBoard();
    updateStatus();
    return true;
  }

  function reset() {
    board = ['', '', '', '', '', '', '', '', ''];
    currentPlayer = 'X';
    gameOver = false;
    winningLine = null;
    renderBoard();
    updateStatus();
  }

  function handleCellClick(event) {
    var cell = event.target;
    if (!cell.classList.contains('cell')) return;
    var index = parseInt(cell.getAttribute('data-index'), 10);
    makeMove(index);
  }

  gridEl.addEventListener('click', handleCellClick);
  restartBtn.addEventListener('click', reset);

  renderBoard();
  updateStatus();
})();
