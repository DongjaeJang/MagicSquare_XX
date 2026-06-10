from entity.constants import MAGIC, GRID_SIZE

__all__ = ["MAGIC", "validate_lines"]


def validate_lines(grid: list[list[int]]) -> dict:
    """10선(R1~R4, C1~C4, D1, D2) 합 검증.

    Returns:
        {
            "status": "pass" | "fail" | "incomplete",
            "failed_lines": [{"id": str, "sum": int, "expected": 34}, ...],
        }
        incomplete 시 failed_lines는 [].
    """
    if any(cell == 0 for row in grid for cell in row):
        return {"status": "incomplete", "failed_lines": []}

    failed_lines: list[dict] = []

    for row_idx in range(GRID_SIZE):
        row_sum = sum(grid[row_idx])
        if row_sum != MAGIC:
            failed_lines.append(
                {"id": f"row:{row_idx}", "sum": row_sum, "expected": MAGIC}
            )

    for col_idx in range(GRID_SIZE):
        col_sum = sum(grid[row_idx][col_idx] for row_idx in range(GRID_SIZE))
        if col_sum != MAGIC:
            failed_lines.append(
                {"id": f"col:{col_idx}", "sum": col_sum, "expected": MAGIC}
            )

    main_sum = sum(grid[i][i] for i in range(GRID_SIZE))
    if main_sum != MAGIC:
        failed_lines.append(
            {"id": "diag:main", "sum": main_sum, "expected": MAGIC}
        )

    anti_sum = sum(grid[i][GRID_SIZE - 1 - i] for i in range(GRID_SIZE))
    if anti_sum != MAGIC:
        failed_lines.append(
            {"id": "diag:anti", "sum": anti_sum, "expected": MAGIC}
        )

    status = "pass" if not failed_lines else "fail"
    return {"status": status, "failed_lines": failed_lines}
