# Tic Tac Toe — Implementation Plan

- **Structure**: Single-page layout with semantic HTML: a 3×3 grid of cells, a status line for turn/winner/draw, and a reset button.
- **State**: Track `board` (array of 9 values: `''`, `'X'`, or `'O'`), `currentPlayer` (`'X'` or `'O'`), and `gameOver` boolean; no persistence.
- **Rendering**: One function to sync the DOM with state: update cell text, disable cells when game over, and set status text (e.g. "X's turn", "O wins!", "Draw").
- **Input**: Single delegated click handler on the grid container; on cell click, if cell is empty and not game over, update state, check win/draw, toggle player, then re-render.
- **Win/draw logic**: Check all 8 lines (3 rows, 3 cols, 2 diagonals) for same non-empty value; if none, check if all 9 cells filled → draw; otherwise game continues.
- **Reset**: Button clears board state, sets `currentPlayer` to `'X'`, `gameOver` to false, and re-renders so the grid is playable again.
- **Styling**: CSS for a clear 3×3 grid, distinct cell hover/click states, and readable status/reset; no external assets or libraries.
- **Edge cases**: Prevent moves after game over; ignore clicks on already-filled cells; declare draw only when board is full with no winner.
