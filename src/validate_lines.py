MAGIC = 34


def validate_lines(grid: list[list[int]]) -> dict:
    """10선(R1~R4, C1~C4, D1, D2) 합 검증.

    Returns:
        {
            "status": "pass" | "fail" | "incomplete",
            "failed_lines": [{"id": str, "sum": int, "expected": 34}, ...],
        }
        incomplete 시 failed_lines는 [].
    """
    ...
