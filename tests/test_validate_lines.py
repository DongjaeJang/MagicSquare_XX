from _approval import assert_matches_golden, canonicalize_approval
from validate_lines import MAGIC, validate_lines

VALID_GRID = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]


def test_pass_when_all_ten_lines_sum_to_magic():
    # Arrange: 10선 모두 합 34인 완성 격자
    grid = VALID_GRID

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "pass"
    assert result["failed_lines"] == []
    assert_matches_golden(
        canonicalize_approval(result, grid=grid),
        "t1.approved.txt",
    )


def test_incomplete_when_grid_contains_zero():
    # Arrange: R5 — 빈칸(0) 포함
    grid = [row[:] for row in VALID_GRID]
    grid[0][0] = 0

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "incomplete"
    assert result["failed_lines"] == []
    assert_matches_golden(
        canonicalize_approval(result, grid=grid),
        "t2.approved.txt",
    )


def test_fail_reports_wrong_line_id_and_sum():
    # Arrange: row:0·col:1 합이 34가 아님 (대각선 비포함 셀)
    grid = [row[:] for row in VALID_GRID]
    grid[0][1] = 99

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["failed_lines"] == [
        {"id": "row:0", "sum": 16 + 99 + 2 + 13, "expected": MAGIC},
        {"id": "col:1", "sum": 99 + 10 + 6 + 15, "expected": MAGIC},
    ]
    assert result["status"] == "fail"
    assert_matches_golden(
        canonicalize_approval(result, grid=grid),
        "t3.approved.txt",
    )
