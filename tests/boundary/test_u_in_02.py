from boundary.input_handler import InputHandler


def test_u_in_02_invalid_size_returns_e001():
    # Given: 3×4 격자
    grid = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
    ]
    handler = InputHandler()
    # When: validate 호출
    result = handler.validate(grid)
    # Then: E001
    assert result["error_code"] == "E001"
