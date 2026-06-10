# TDD RED — `validate_lines`

MagicSquare_XX 세션 3. **RED 단계 전용** — 실패하는 테스트만 추가한다.
프로젝트 규칙: `.cursorrules` 준수.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 작성:

```
Phase: RED
```

이후 본문을 이어간다. GREEN·REFACTOR 내용은 쓰지 않는다.

---

## RED 범위

| 허용 | 금지 |
|------|------|
| `tests/test_validate_lines.py` 수정·추가 | `src/` **어떤 파일도** 수정 |
| `pytest` 실행·실패 확인 | `validate_lines` 구현·`...` 제거 |
| 격자 fixture·헬퍼를 `tests/` 안에 정의 | assert 완화·삭제·조건 완화 |
| | `@pytest.mark.skip`, `xfail`, `pass` placeholder |
| | GREEN/REFACTOR 선행, `git commit` (사용자 요청 전) |

**성공 기준:** `pytest`가 **의도적으로 FAILED** 상태여야 RED 완료.

---

## AAA 절차

각 테스트 함수는 **Arrange → Act → Assert** 순서를 따른다.

1. **Arrange** — 4×4 `grid` 준비. 셀은 `0`(빈칸) 또는 `1~16`. 시나리오를 주석으로 명시.
2. **Act** — `result = validate_lines(grid)` 한 번 호출.
3. **Assert** — 반환 dict를 **직접** 검증 (Boundary 없음).

### API 계약 (assert 대상)

```python
result = {
    "status": "pass" | "fail" | "incomplete",
    "failed_lines": [{"id": str, "sum": int, "expected": 34}, ...],
}
```

- `pass` — 10선(R1~R4, C1~C4, D1·D2) 모두 합 34
- `fail` — `0` 없음, 하나 이상 합 ≠ 34 → **틀린 줄만** `failed_lines`
- `incomplete` — `0` 하나라도 있음 → `status=="incomplete"`, `failed_lines==[]`
- 줄 ID: `row:0`~`row:3`, `col:0`~`col:3`, `diag:main`, `diag:anti`
- `MAGIC = 34` — `from validate_lines import MAGIC, validate_lines`

---

## pytest 예시

`tests/test_validate_lines.py`에 아래 패턴으로 작성한다.

```python
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


def test_incomplete_when_grid_contains_zero():
    # Arrange: R5 — 빈칸(0) 포함
    grid = [row[:] for row in VALID_GRID]
    grid[0][0] = 0

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "incomplete"
    assert result["failed_lines"] == []


def test_fail_reports_wrong_line_id_and_sum():
    # Arrange: row:0 합이 34가 아님
    grid = [row[:] for row in VALID_GRID]
    grid[0][0] = 99

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "fail"
    assert result["failed_lines"] == [
        {"id": "row:0", "sum": 99 + 3 + 2 + 13, "expected": MAGIC},
    ]
```

실행:

```bash
python -m pytest tests/test_validate_lines.py -v
```

RED 완료 시 위 테스트들이 **FAILED** (또는 ERROR)여야 한다.

---

## 작업 순서

1. 사용자 요청·Mom Test 시나리오에서 **하나의 실패 조건**을 고른다.
2. `tests/test_validate_lines.py`에 AAA 테스트 **하나**(또는 요청된 범위)를 추가한다.
3. `python -m pytest tests/test_validate_lines.py -v` 실행한다.
4. 실패 메시지가 **assert 기대값**과 일치하는지 확인한다.
5. 아래 보고 형식으로 결과를 제출한다.

---

## 보고 형식 (필수)

```markdown
Phase: RED

## 추가한 테스트
- `test_...` — [시나리오 한 줄: pass / fail / incomplete 중 무엇을 검증]

## Arrange 요약
- 격자 상태: [예: VALID_GRID, row:0 한 칸 오류, 0 포함 등]

## 기대 실패
- [pytest가 실패해야 하는 이유 — 구현 없음 / status 불일치 등]

## pytest 결과
[FAILED/ERROR 요약 1~3줄. 핵심 assert 메시지 인용]

## 변경 파일
- `tests/test_validate_lines.py` (+N줄)

## 다음 단계
- GREEN: `/tdd-green` 또는 사용자 요청 시 `src/validate_lines.py` 최소 구현
```

---

## 금지 사항 (재확인)

- `src/validate_lines.py` 및 `src/` 전체 **수정 금지**
- 기존 assert를 느슨하게 바꿔 GREEN을 우회하는 행위 **금지**
- Solver, GridUI, ECB 전체, 1~16 중복 검증 등 **세션 3 범위 밖** 테스트 **금지**
- 한국어로 응답

---

## 컨텍스트

명령 뒤에 붙은 텍스트(예: `/tdd-red incomplete 케이스`)가 있으면 **그 시나리오를 우선**하여 테스트를 작성한다.
