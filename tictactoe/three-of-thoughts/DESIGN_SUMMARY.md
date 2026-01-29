# Design Decision Summary

## Tree-of-Thoughts choices

| Area | Strategy chosen | Why |
|------|-----------------|-----|
| **HTML board** | 9 `<button>` elements in a wrapper, each with `data-index="0"`–`"8"` | Semantic, accessible, one listener per cell or delegation. |
| **Board styling** | CSS Grid (`grid-template-columns: repeat(3, 1fr)`) | Equal 3×3 layout with minimal code; Flexbox would need explicit widths. |
| **Game state** | Module-level variables: `board` (flat array of 9), `currentPlayer`, `gameOver`, `mode` | Single source of truth, simple reset, no framework. |
| **Turns** | Toggle `currentPlayer` after each valid move; X always starts. | Clear and easy to reset. |
| **Win detection** | Eight hardcoded lines (3 rows, 3 cols, 2 diagonals); check after each move. | Correct and readable for 3×3. |
| **Draw** | No winner and `board.every(cell => cell !== '')`. | Covers all draw edge cases. |
| **AI** | Easy = random empty cell. Medium = win if possible → block → else random. | Simple, no minimax; good balance. |

**Alternatives not chosen:** 2D array (unnecessary), DOM-as-state (harder to test), Flexbox (Grid fits 3×3 better), minimax (overkill for ~150-line goal).
