# Tic Tac Toe

A two-player tic tac toe game in the browser.

## How to play

1. Open `index.html` in a browser (double-click or drag into a tab), or run a local server:
   ```bash
   npx serve .
   ```
2. Players take turns clicking a cell. X goes first.
3. Get three in a row (horizontal, vertical, or diagonal) to win.
4. Use **New game** to clear the board and keep playing. Win/draw counts are kept across games.

## Files

- `index.html` – Page structure and board
- `styles.css` – Layout and theme (dark UI, X in amber, O in cyan)
- `game.js` – Turn handling, win/draw detection, score tracking
