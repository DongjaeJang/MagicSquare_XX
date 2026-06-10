from entity.find_blank_coords import find_blank_coords
from _approval import assert_matches_golden, format_coord_list


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given: G1 격자 (0이 2개)
    # When: find_blank_coords(grid_g1) 호출
    actual = find_blank_coords(grid_g1)
    # Then: [(2,3),(4,4)] 반환 (1-index, row-major) — Golden Master
    assert_matches_golden(
        format_coord_list(actual),
        "d_loc_01_g1_blank_coords.approved.txt",
    )
