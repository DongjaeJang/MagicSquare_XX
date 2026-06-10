import pytest

from entity.constants import BLANK_CELL

# G1 SSOT — 빈칸 1-index (2,3), (4,4) → 0-index (1,2), (3,3)
GRID_G1 = [
    [16, 3, 2, 13],
    [5, 10, BLANK_CELL, 11],
    [9, 6, 7, 12],
    [4, 15, 14, BLANK_CELL],
]


@pytest.fixture
def grid_g1() -> list[list[int]]:
    return [row[:] for row in GRID_G1]
