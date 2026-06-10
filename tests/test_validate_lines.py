from validate_lines import MAGIC, validate_lines

VALID_GRID = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]


def test_pass_when_all_ten_lines_sum_to_magic():
    grid = VALID_GRID
    result = validate_lines(grid)
    assert result["status"] == "pass"
    assert result["failed_lines"] == []


def test_incomplete_when_grid_contains_zero():
    grid = [row[:] for row in VALID_GRID]
    grid[0][0] = 0
    result = validate_lines(grid)
    assert result["status"] == "incomplete"
    assert result["failed_lines"] == []


def test_fail_reports_wrong_line_id_and_sum():
    grid = [row[:] for row in VALID_GRID]
    grid[0][0] = 99
    result = validate_lines(grid)
    assert result["status"] == "fail"
    assert result["failed_lines"] == [
        {"id": "row:0", "sum": 99 + 3 + 2 + 13, "expected": MAGIC},
    ]
