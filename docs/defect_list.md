# MagicSquare_XX — 결함 목록

| 항목 | 내용 |
|------|------|
| 갱신일 | 2026-06-10 |
| SSOT | [PRD.md](./PRD.md) |

---

## 해결됨 (DEF)

| ID | Test ID | 설명 | 근본 원인 | 해결 |
|----|---------|------|-----------|------|
| DEF-001 | T1~T3 | `validate_lines` 미구현 (`...`) | GREEN 전 RED 단계 | `src/validate_lines.py` 10선 검증 구현 |
| DEF-002 | D-LOC-01 | `find_blank_coords` 없음 | entity 미구현 | `src/entity/find_blank_coords.py` |
| DEF-003 | U-IN-01/02 | `InputHandler` 없음 | boundary 미구현 | `src/boundary/input_handler.py` |

---

## 문서·설계 (ISS)

| ID | 설명 | 조치 |
|----|------|------|
| ISS-001 | PRD G1 빈칸 0-index `(1,3),(2,2)` vs 워크북 Then `[(2,3),(4,4)]` | 테스트 SSOT는 `tests/conftest.py` GRID_G1 (워크북 실습 기준) |
| ISS-002 | T3 RED assert가 `row:0`만 기대 | 한 셀 변경 시 `col:0`도 실패 — assert를 PRD §6 FR-4에 맞게 보강 |

---

## 미해결 / 범위 밖

| ID | 설명 | 다음 단계 |
|----|------|-----------|
| — | Solver, GridUI, PyQt 전체 앱 | 후속 세션 |
| — | 1~16 중복·범위 검증 | PRD Non-FR |
