# Tic Tac Toe — Acceptance Checklist

- [ ] **Grid**: 3×3 playable grid; each cell shows nothing, X, or O.
- [ ] **Turns**: X goes first; turns alternate after each valid move.
- [ ] **Win**: When a player gets three in a row (any row, column, or diagonal), game ends and status shows winner (e.g. "X wins!" or "O wins!").
- [ ] **Draw**: When all nine cells are filled and there is no winner, game ends and status shows "Draw".
- [ ] **No move after game over**: Once win or draw is detected, no further moves are allowed until reset.
- [ ] **Ignore invalid clicks**: Clicking an already-filled cell does nothing.
- [ ] **Reset**: A reset/restart button clears the board and restarts the game (X first); grid and status update correctly.
- [ ] **No libraries**: Implemented with plain HTML, CSS, and JavaScript only (no frameworks or external scripts).
- [ ] **JS size**: `app.js` is under ~150 lines (excluding blank/comment lines if desired).
