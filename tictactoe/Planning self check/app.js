(function () {
  'use strict';

  var LINES = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
  ];

  var board = ['', '', '', '', '', '', '', '', ''];
  var currentPlayer = 'X';
  var gameOver = false;

  var statusEl = document.getElementById('status');
  var gridEl = document.getElementById('grid');
  var resetEl = document.getElementById('reset');

  function getWinner() {
    for (var i = 0; i < LINES.length; i++) {
      var a = LINES[i][0], b = LINES[i][1], c = LINES[i][2];
      var v = board[a];
      if (v && v === board[b] && v === board[c]) return v;
    }
    return null;
  }

  function isDraw() {
    for (var i = 0; i < 9; i++) if (!board[i]) return false;
    return true;
  }

  function render() {
    var winner = getWinner();
    var draw = isDraw();

    if (winner) {
      statusEl.textContent = winner + ' wins!';
      gameOver = true;
    } else if (draw) {
      statusEl.textContent = 'Draw';
      gameOver = true;
    } else {
      statusEl.textContent = currentPlayer + "'s turn";
    }

    var cells = gridEl.querySelectorAll('.cell');
    for (var i = 0; i < 9; i++) {
      var cell = cells[i];
      cell.textContent = board[i];
      cell.dataset.value = board[i] || '';
      cell.disabled = !!gameOver;
    }

    if (gameOver) resetEl.focus({ preventScroll: true });
  }

  function makeMove(index) {
    if (gameOver || board[index]) return;
    board[index] = currentPlayer;
    var winner = getWinner();
    var draw = isDraw();
    if (!winner && !draw) currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
    render();
  }

  function reset() {
    board = ['', '', '', '', '', '', '', '', ''];
    currentPlayer = 'X';
    gameOver = false;
    render();
  }

  gridEl.addEventListener('click', function (e) {
    var cell = e.target.closest('.cell');
    if (!cell) return;
    var index = parseInt(cell.dataset.index, 10);
    if (!isNaN(index)) makeMove(index);
  });

  resetEl.addEventListener('click', reset);

  render();
})();
