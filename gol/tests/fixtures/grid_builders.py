"""Build grid fixtures for testing (dtype uint8, 0/1)."""
import numpy as np

DTYPE = np.uint8


def blank_grid(rows: int = 5, cols: int = 5) -> np.ndarray:
    """Return a blank grid of given shape."""
    return np.zeros((rows, cols), dtype=DTYPE)


def single_live_center(rows: int = 3, cols: int = 3) -> np.ndarray:
    """Grid with a single live cell at center."""
    g = np.zeros((rows, cols), dtype=DTYPE)
    g[rows // 2, cols // 2] = 1
    return g


def grid_with_live_cell(row: int, col: int, rows: int = 5, cols: int = 5) -> np.ndarray:
    """Grid with one live cell at (row, col)."""
    g = np.zeros((rows, cols), dtype=DTYPE)
    g[row, col] = 1
    return g


def blinker_horizontal(rows: int = 5, cols: int = 5, r: int = 2, c: int = 1) -> np.ndarray:
    """Horizontal blinker (3 cells in a row); period-2 oscillator."""
    g = np.zeros((rows, cols), dtype=DTYPE)
    g[r, c], g[r, c + 1], g[r, c + 2] = 1, 1, 1
    return g


def glider_grid(rows: int = 10, cols: int = 10) -> np.ndarray:
    """Grid with a single glider centered."""
    g = np.zeros((rows, cols), dtype=DTYPE)
    r0, c0 = (rows - 3) // 2, (cols - 3) // 2
    g[r0, c0 + 1] = 1
    g[r0 + 1, c0 + 2] = 1
    g[r0 + 2, c0], g[r0 + 2, c0 + 1], g[r0 + 2, c0 + 2] = 1, 1, 1
    return g
