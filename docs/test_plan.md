# MagicSquare_XX — 테스트 플랜 (TC-MS)

| 항목 | 내용 |
|------|------|
| SSOT | [PRD.md](./PRD.md) §6·§7 |
| 갱신일 | 2026-06-10 |
| 상태 | Track A·B GREEN PASS |

---

## 1. FR ↔ Test ID 매핑

| FR | Test ID | 파일 | Given → Then |
|----|---------|------|--------------|
| FR-1 | T1 | `tests/test_validate_lines.py` | VALID_GRID → `pass`, `[]` |
| FR-3 | T2 | 동일 | `0` 포함 → `incomplete`, `[]` |
| FR-4·FR-5 | T3 | 동일 | row:0·col:0 오류 → `fail`, 줄별 sum |
| FR-LOC-01 | D-LOC-01 | `tests/entity/test_d_loc_01.py` | G1 → `[(2,3),(4,4)]` 1-index |
| — | U-IN-01 | `tests/boundary/test_u_in_01.py` | `grid=None` → `E003` |
| — | U-IN-02 | `tests/boundary/test_u_in_02.py` | `3×4` → `E001` |

---

## 2. RED 묶음 이력

| 묶음 | Test ID | Phase | 결과 |
|------|---------|-------|------|
| 1 | T1~T3 | RED → GREEN | PASS |
| 2 | D-LOC-01 | RED → GREEN | PASS + Golden matched |
| 3 | U-IN-01, U-IN-02 | RED → GREEN | PASS |

---

## 3. Golden Master

| Test ID | golden 경로 | matched |
|---------|-------------|---------|
| D-LOC-01 | `tests/golden/d_loc_01_g1_blank_coords.approved.txt` | ✅ |

포맷: 1-index `row,col` 줄당 1좌표 (I6 row-major).

---

## 4. AC 대비

| AC | 기준 | 상태 |
|----|------|------|
| AC-1 | FR-1 T1 pass | ✅ |
| AC-2 | FR-3 T2 incomplete | ✅ |
| AC-3 | FR-4·5 T3 failed_lines | ✅ |
| AC-4 | `pytest tests/` 전부 PASS | ✅ |
| AC-5 | golden matched | ✅ |

---

## 5. RED 후보 (다음 사이클)

| Test ID | 대상 | Given → Then |
|---------|------|--------------|
| T4 | `validate_lines` | `diag:main` 실패 |
| T5 | `validate_lines` | 복수 `failed_lines` 정렬 |
| D-MIS-01 | `find_not_exist_nums` | G1 → `[7,10]` |
| U-IN-03 | `InputHandler` | 빈칸 0개 → `E002` |
