from boundary.input_handler import InputHandler


def test_u_in_01_null_grid_returns_e003():
    # Given: grid=None
    handler = InputHandler()
    # When: validate 호출
    result = handler.validate(None)
    # Then: E003
    assert result["error_code"] == "E003"
