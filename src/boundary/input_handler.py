from entity.constants import BLANK_CELL, GRID_SIZE, MAX_CELL_VALUE


class InputHandler:
    def validate(self, grid: list[list[int]] | None) -> dict:
        if grid is None:
            return {"error_code": "E003"}
        if len(grid) != GRID_SIZE or any(len(row) != GRID_SIZE for row in grid):
            return {"error_code": "E001"}
        for row in grid:
            for cell in row:
                if cell != BLANK_CELL and not (1 <= cell <= MAX_CELL_VALUE):
                    return {"error_code": "E002"}
        return {"error_code": None}
