"""
Conway's Game of Life — Streamlit app.
Engine (pure, vectorized) in ENGINE section; UI uses session_state only.
"""
from __future__ import annotations

import time
from typing import Any

import numpy as np
import streamlit as st
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

from common.logging import get_logger

logger = get_logger(__name__)

# -----------------------------------------------------------------------------
# ENGINE — Pure simulation (NumPy, no UI)
# -----------------------------------------------------------------------------

DTYPE = np.uint8


def count_neighbors_wrap(grid: np.ndarray) -> np.ndarray:
    """Count live neighbors with toroidal wrap via np.roll in 8 directions."""
    out = np.zeros(grid.shape, dtype=DTYPE)
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            out += np.roll(np.roll(grid, dr, axis=0), dc, axis=1)
    return out


def count_neighbors_no_wrap(grid: np.ndarray) -> np.ndarray:
    """Count live neighbors without wrap; outside = dead. Zero-pad and slice."""
    padded = np.zeros((grid.shape[0] + 2, grid.shape[1] + 2), dtype=DTYPE)
    padded[1:-1, 1:-1] = grid
    out = (
        padded[0:-2, 0:-2] + padded[0:-2, 1:-1] + padded[0:-2, 2:]
        + padded[1:-1, 0:-2] + padded[1:-1, 2:]
        + padded[2:, 0:-2] + padded[2:, 1:-1] + padded[2:, 2:]
    )
    return out


def next_generation(grid: np.ndarray, wrap: bool) -> np.ndarray:
    """Survival 2–3, birth 3, else dead."""
    n = count_neighbors_wrap(grid) if wrap else count_neighbors_no_wrap(grid)
    return ((grid == 1) & (n >= 2) & (n <= 3) | ((grid == 0) & (n == 3))).astype(DTYPE)


def _glider() -> np.ndarray:
    a = np.zeros((3, 3), dtype=DTYPE)
    a[0, 1], a[1, 2], a[2, 0], a[2, 1], a[2, 2] = 1, 1, 1, 1, 1
    return a


def _lwss() -> np.ndarray:
    a = np.zeros((4, 5), dtype=DTYPE)
    a[0, 1], a[0, 2], a[0, 3], a[0, 4] = 1, 1, 1, 1
    a[1, 0], a[1, 1], a[1, 2], a[1, 3] = 1, 1, 1, 1
    a[2, 1], a[2, 2], a[2, 3] = 1, 1, 1
    a[3, 0], a[3, 2] = 1, 1
    return a


def _gosper_glider_gun() -> np.ndarray:
    gun = np.zeros((9, 36), dtype=DTYPE)
    for c in (0, 1, 10, 11):
        gun[4, c] = 1
    for c in (0, 1, 10, 11):
        gun[5, c] = 1
    for c in (20, 21, 22):
        gun[4, c], gun[5, c] = 1, 1
    gun[5, 23], gun[6, 22], gun[6, 23], gun[6, 24] = 1, 1, 1, 1
    gun[4, 34], gun[4, 35], gun[5, 34], gun[5, 35] = 1, 1, 1, 1
    for r in (2, 3):
        gun[r, 24] = 1
    for r in (2, 3):
        gun[r, 22] = 1
    gun[3, 20], gun[3, 21], gun[4, 20], gun[4, 21] = 1, 1, 1, 1
    return gun


def _pulsar() -> np.ndarray:
    a = np.zeros((13, 13), dtype=DTYPE)
    for (r, c) in [
        (0, 2), (0, 3), (0, 4), (0, 8), (0, 9), (0, 10),
        (2, 0), (2, 5), (2, 7), (2, 12), (3, 0), (3, 5), (3, 7), (3, 12),
        (4, 0), (4, 5), (4, 7), (4, 12), (5, 2), (5, 3), (5, 4), (5, 8), (5, 9), (5, 10),
        (7, 2), (7, 3), (7, 4), (7, 8), (7, 9), (7, 10), (8, 0), (8, 5), (8, 7), (8, 12),
        (9, 0), (9, 5), (9, 7), (9, 12), (10, 0), (10, 5), (10, 7), (10, 12),
        (12, 2), (12, 3), (12, 4), (12, 8), (12, 9), (12, 10),
    ]:
        a[r, c] = 1
    return a


PRESETS: dict[str, Any] = {
    "Blank": None,
    "Random": "density",
    "Glider": _glider(),
    "Lightweight Spaceship": _lwss(),
    "Gosper Glider Gun": _gosper_glider_gun(),
    "Pulsar": _pulsar(),
}


def build_initial_grid(
    rows: int,
    cols: int,
    preset_key: str,
    density: float = 0.3,
    rng: np.random.Generator | None = None,
) -> tuple[np.ndarray, str | None]:
    """Return (grid, error_message). If preset too large, return warning and empty grid."""
    if rows <= 0 or cols <= 0:
        return np.zeros((max(1, rows), max(1, cols)), dtype=DTYPE), "Invalid grid size."
    grid = np.zeros((rows, cols), dtype=DTYPE)
    if preset_key == "Blank":
        return grid, None
    if preset_key == "Random":
        rng = rng or np.random.default_rng()
        grid[:, :] = (rng.random((rows, cols)) < density).astype(DTYPE)
        return grid, None
    pattern = PRESETS.get(preset_key)
    if pattern is None or not isinstance(pattern, np.ndarray):
        return grid, None
    ph, pw = pattern.shape
    if ph > rows or pw > cols:
        return grid, f"Grid too small for preset. Needs at least {ph}×{pw}; grid is {rows}×{cols}."
    r0, c0 = (rows - ph) // 2, (cols - pw) // 2
    grid[r0 : r0 + ph, c0 : c0 + pw] = pattern
    return grid, None


def self_check_neighbors() -> bool:
    g = np.zeros((3, 3), dtype=DTYPE)
    g[1, 1], g[0, 1] = 1, 1
    nw = count_neighbors_wrap(g)
    nn = count_neighbors_no_wrap(g)
    assert nw[1, 1] == 1 and nn[1, 1] == 1
    assert nw[0, 0] == 2 and nn[0, 0] == 2
    return True


def self_check_preset_bounds() -> bool:
    _, err = build_initial_grid(2, 2, "Glider")
    assert err is not None and "too small" in err.lower()
    g, err = build_initial_grid(10, 10, "Glider")
    # Glider has no cell at center (1,1); live cells include (0,1)->(3,4) and (2,2)->(5,5)
    assert err is None and g[3, 4] == 1 and g.sum() == 5
    return True


# -----------------------------------------------------------------------------
# UI — Streamlit
# -----------------------------------------------------------------------------


def _default_state() -> None:
    defaults = {
        "grid": np.zeros((50, 50), dtype=DTYPE),
        "playing": False,
        "speed_ms": 200,
        "generation": 0,
        "wrap": False,
        "cell_size": 8,
        "rows": 50,
        "cols": 50,
        "edit_mode": "Toggle",
        "brush_size": 1,
        "last_tick": time.time(),
        "preset": "Blank",
        "density": 0.3,
        "click_key": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _grid_to_image(grid: np.ndarray, cell_size: int) -> Image.Image:
    expanded = np.repeat(np.repeat(grid, cell_size, axis=0), cell_size, axis=1)
    img = np.where(expanded[:, :, None], (40, 40, 40), (255, 255, 255)).astype(np.uint8)
    return Image.fromarray(img)


def _apply_edit(grid: np.ndarray, row: int, col: int, mode: str, brush: int) -> None:
    h, w = grid.shape
    r0, r1 = max(0, row - brush), min(h, row + brush + 1)
    c0, c1 = max(0, col - brush), min(w, col + brush + 1)
    if mode == "Paint":
        grid[r0:r1, c0:c1] = 1
    elif mode == "Erase":
        grid[r0:r1, c0:c1] = 0
    else:
        grid[r0:r1, c0:c1] = 1 - grid[r0:r1, c0:c1]


def main() -> None:
    st.set_page_config(page_title="Conway's Game of Life", layout="wide")
    _default_state()

    with st.sidebar:
        st.subheader("Grid size")
        rows = st.number_input("Rows", min_value=5, max_value=200, value=st.session_state.rows, step=1)
        cols = st.number_input("Columns", min_value=5, max_value=200, value=st.session_state.cols, step=1)
        cell_size = st.slider("Cell size (px)", 4, 24, st.session_state.cell_size, 2)

        st.subheader("Initial structure")
        preset = st.selectbox("Preset", list(PRESETS.keys()), index=list(PRESETS.keys()).index(st.session_state.preset))
        density = st.session_state.density
        if preset == "Random":
            density = st.slider("Density", 0.0, 1.0, st.session_state.density, 0.05)
            st.session_state.density = density

        if st.button("Apply / Reset"):
            grid, err = build_initial_grid(rows, cols, preset, density=density)
            if err:
                st.session_state.preset_warning = err
            else:
                st.session_state.grid = grid
                st.session_state.rows, st.session_state.cols = rows, cols
                st.session_state.cell_size = cell_size
                st.session_state.preset, st.session_state.density = preset, density
                st.session_state.generation = 0
                st.session_state.pop("preset_warning", None)
            st.rerun()

        st.subheader("Editing")
        edit_mode = st.radio("Mode", ["Toggle", "Paint", "Erase"], index=["Toggle", "Paint", "Erase"].index(st.session_state.edit_mode))
        st.session_state.edit_mode = edit_mode
        st.session_state.brush_size = st.slider("Brush size", 1, 5, st.session_state.brush_size, 1)
        if st.button("Clear"):
            st.session_state.grid = np.zeros((st.session_state.rows, st.session_state.cols), dtype=DTYPE)
            st.session_state.generation = 0
            st.rerun()

        st.subheader("Simulation")
        if st.button("Pause" if st.session_state.playing else "Play"):
            st.session_state.playing = not st.session_state.playing
            st.session_state.last_tick = time.time()
            st.rerun()
        if st.button("Step"):
            st.session_state.grid = next_generation(st.session_state.grid, st.session_state.wrap)
            st.session_state.generation += 1
            st.rerun()

        st.session_state.speed_ms = st.slider("Speed (ms per tick)", 50, 1000, st.session_state.speed_ms, 50)
        st.session_state.wrap = st.checkbox("Toroidal wrap", value=st.session_state.wrap)

    if st.session_state.get("preset_warning"):
        st.warning(st.session_state.preset_warning)

    st.caption(f"Generation: {st.session_state.generation}  |  Wrap: {'On' if st.session_state.wrap else 'Off'}")

    img = _grid_to_image(st.session_state.grid, st.session_state.cell_size)
    event = streamlit_image_coordinates(img, key=f"grid_{st.session_state.click_key}")
    if event and event.get("x") is not None and event.get("y") is not None:
        c = int(event["x"]) // st.session_state.cell_size
        r = int(event["y"]) // st.session_state.cell_size
        if 0 <= r < st.session_state.grid.shape[0] and 0 <= c < st.session_state.grid.shape[1]:
            _apply_edit(st.session_state.grid, r, c, st.session_state.edit_mode, st.session_state.brush_size)
            st.session_state.click_key += 1
            st.rerun()

    try:
        self_check_neighbors()
        self_check_preset_bounds()
    except Exception:
        logger.exception("self_check_failed")

    if st.session_state.playing:
        if time.time() - st.session_state.last_tick >= st.session_state.speed_ms / 1000.0:
            st.session_state.grid = next_generation(st.session_state.grid, st.session_state.wrap)
            st.session_state.generation += 1
            st.session_state.last_tick = time.time()
        time.sleep(st.session_state.speed_ms / 1000.0)
        st.rerun()


if __name__ == "__main__":
    main()
