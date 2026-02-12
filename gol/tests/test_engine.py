"""Tests for Game of Life engine."""
import numpy as np
import pytest

from app import (
    PRESETS,
    build_initial_grid,
    count_neighbors_no_wrap,
    count_neighbors_wrap,
    next_generation,
    self_check_neighbors,
    self_check_preset_bounds,
)
from tests.fixtures import (
    blank_grid,
    blinker_horizontal,
    glider_grid,
    grid_with_live_cell,
    single_live_center,
)


class TestCountNeighborsWrap:
    def test_single_live_center_has_one_neighbor(self) -> None:
        g = single_live_center(3, 3)
        n = count_neighbors_wrap(g)
        assert n[1, 1] == 1

    def test_corner_with_wrap_sees_wrapped_neighbors(self) -> None:
        g = grid_with_live_cell(1, 1, 3, 3)
        n = count_neighbors_wrap(g)
        assert n[0, 0] == 2

    def test_all_dead_returns_zeros(self) -> None:
        g = blank_grid(4, 4)
        n = count_neighbors_wrap(g)
        np.testing.assert_array_equal(n, 0)


class TestCountNeighborsNoWrap:
    def test_single_live_center_has_one_neighbor(self) -> None:
        g = single_live_center(3, 3)
        n = count_neighbors_no_wrap(g)
        assert n[1, 1] == 1

    def test_corner_cell_no_wrap(self) -> None:
        g = grid_with_live_cell(1, 1, 3, 3)
        n = count_neighbors_no_wrap(g)
        assert n[0, 0] == 2

    def test_isolated_cell_has_zero_neighbors(self) -> None:
        g = np.zeros((5, 5), dtype=np.uint8)
        g[2, 2] = 1
        n = count_neighbors_no_wrap(g)
        assert n[2, 2] == 0


class TestNextGeneration:
    def test_blinker_oscillates_no_wrap(self) -> None:
        g = blinker_horizontal(5, 5, 2, 1)
        g1 = next_generation(g, wrap=False)
        assert g1[1, 2] == 1 and g1[2, 2] == 1 and g1[3, 2] == 1
        g2 = next_generation(g1, wrap=False)
        np.testing.assert_array_equal(g2[2, 1:4], [1, 1, 1])

    def test_survival_with_2_neighbors(self) -> None:
        g = np.zeros((3, 3), dtype=np.uint8)
        g[0, 0], g[0, 1], g[1, 0] = 1, 1, 1
        g1 = next_generation(g, wrap=False)
        assert g1[0, 0] == 1

    def test_birth_with_exactly_3_neighbors(self) -> None:
        g = np.zeros((3, 3), dtype=np.uint8)
        g[0, 0], g[0, 1], g[1, 0] = 1, 1, 1
        g1 = next_generation(g, wrap=False)
        assert g1[1, 1] == 1

    def test_death_by_underpopulation(self) -> None:
        g = grid_with_live_cell(2, 2, 5, 5)
        g1 = next_generation(g, wrap=False)
        assert g1[2, 2] == 0


class TestBuildInitialGrid:
    def test_blank_returns_zeros(self) -> None:
        grid, err = build_initial_grid(10, 10, "Blank")
        assert err is None
        np.testing.assert_array_equal(grid, 0)

    def test_random_returns_grid(self) -> None:
        rng = np.random.default_rng(42)
        grid, err = build_initial_grid(20, 20, "Random", density=0.5, rng=rng)
        assert err is None
        assert 0 < grid.sum() < 400

    def test_glider_centered(self) -> None:
        grid, err = build_initial_grid(10, 10, "Glider")
        assert err is None
        assert grid[4, 4] == 1

    def test_glider_too_small_returns_error(self) -> None:
        grid, err = build_initial_grid(2, 2, "Glider")
        assert err is not None
        assert "too small" in err.lower()

    def test_invalid_size_returns_error(self) -> None:
        _, err = build_initial_grid(0, 5, "Blank")
        assert err is not None

    def test_pulsar_requires_at_least_13x13(self) -> None:
        _, err = build_initial_grid(12, 12, "Pulsar")
        assert err is not None
        grid, err = build_initial_grid(13, 13, "Pulsar")
        assert err is None
        assert grid.sum() > 0


class TestPresetShapes:
    def test_glider_is_3x3(self) -> None:
        p = PRESETS["Glider"]
        assert p is not None and hasattr(p, "shape")
        assert p.shape == (3, 3)

    def test_pulsar_is_13x13(self) -> None:
        p = PRESETS["Pulsar"]
        assert p is not None and hasattr(p, "shape")
        assert p.shape == (13, 13)


class TestSelfChecks:
    def test_self_check_neighbors_passes(self) -> None:
        assert self_check_neighbors() is True

    def test_self_check_preset_bounds_passes(self) -> None:
        assert self_check_preset_bounds() is True
