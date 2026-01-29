# Tic Tac Toe

A small Tic Tac Toe game built with plain HTML, CSS, and JavaScript (no frameworks).

## Run locally

1. Open the project folder in your terminal.
2. Serve the folder with any static server, or open `index.html` in a browser.

**Option A – Python 3**
```bash
cd "Prompt B"
python3 -m http.server 8000
```
Then open http://localhost:8000 in your browser.

**Option B – Node (npx)**
```bash
cd "Prompt B"
npx serve .
```
Then open the URL shown in the terminal (e.g. http://localhost:3000).

**Option C – Direct file**
Double-click `index.html` or drag it into a browser window. Some features may be limited when using `file://`.

## Files

- `index.html` – Page structure and 3×3 grid
- `style.css` – Layout and styling (including winning-line highlight)
- `app.js` – Game logic: `makeMove`, `checkWinner`, `reset`

## How to play

- Click a cell to place X or O (X goes first).
- First to get three in a row (horizontal, vertical, or diagonal) wins.
- The winning line is highlighted in green.
- Use **Restart** to play again. Moves are disabled after a win or draw.
