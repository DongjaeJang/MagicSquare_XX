"""Approval test helpers — golden file compare."""

from __future__ import annotations

import os
from pathlib import Path

from entity.constants import BLANK_CELL, MAGIC

GOLDEN_DIR = Path(__file__).resolve().parent / "golden"

_LINE_SORT = (
    lambda lid: (
        0 if lid.startswith("row:") else 1 if lid.startswith("col:") else 2,
        lid,
    )
)


def canonicalize_approval(result: dict, *, grid: list[list[int]] | None = None) -> str:
    status = result["status"]
    int6 = _blank_int6(grid or [], result)
    codes = _codes_line(result)
    return f"status={status}\nint6={int6}\ncodes={codes}\n"


def _blank_int6(grid: list[list[int]], result: dict) -> str:
    blanks: list[tuple[int, int]] = []
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell == BLANK_CELL:
                blanks.append((row_idx + 1, col_idx + 1))

    if len(blanks) >= 1:
        i1, i2 = blanks[0]
    else:
        i1, i2 = 0, 0
    if len(blanks) >= 2:
        i3, i4 = blanks[1]
    else:
        i3, i4 = 0, 0

    if result["status"] == "fail" and result["failed_lines"]:
        i5 = result["failed_lines"][0]["sum"]
        i6 = MAGIC
    else:
        i5, i6 = 0, 0

    return f"{i1},{i2},{i3},{i4},{i5},{i6}"


def _codes_line(result: dict) -> str:
    status = result["status"]
    if status == "pass":
        return ""
    if status == "incomplete":
        return "INC:zero"
    failed = sorted(result["failed_lines"], key=lambda entry: _LINE_SORT(entry["id"]))
    return "|".join(f"LINE:{entry['id']}" for entry in failed)


def format_coord_list(coords: list[tuple[int, int]]) -> str:
    """1-index row,col per line, row-major, trailing newline."""
    return "\n".join(f"{row},{col}" for row, col in coords) + "\n"


def assert_matches_golden(actual: str, golden_relative: str) -> None:
    """Compare *actual* to tests/golden/{golden_relative}."""
    update = os.environ.get("UPDATE_GOLDEN") == "1"
    golden_path = GOLDEN_DIR / golden_relative
    golden_path.parent.mkdir(parents=True, exist_ok=True)

    if update:
        golden_path.write_text(actual, encoding="utf-8")
        return

    if not golden_path.is_file():
        raise AssertionError(f"golden missing: {golden_path}")

    expected = golden_path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(
            f"golden mismatch: {golden_path}\n--- expected ---\n{expected}--- actual ---\n{actual}"
        )
