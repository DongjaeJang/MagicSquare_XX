# RED Skeleton — ARRR A단계 (RED ④)

MagicSquare_XX **RED ④ 전용** — `/red-test-plan` 설계표(C2C·Track B) 기준으로 **pytest.fail 스켈레톤**만 작성한다.
**assert 본문·구현 연결은 다음 `/tdd-red`에서** 한다.

선행: `/red-test-plan` (RED ③) 완료·4블록 확정.
SSOT: 직전 `/red-test-plan` 출력, `.cursorrules`, `docs/PRD.md`.
**Skill:** `magic-square-tdd` Skill이 있으면 자동 따름.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 작성:

```
Phase: red | Layer: entity | Track: Logic
```

- `Layer`: `entity` (기본) 또는 `boundary` (Track A — `/red-test-plan`과 동일 선언 치환)
- `Track`: `Logic` (기본) 또는 `UI`
- **Track A(boundary):** 선언의 `Layer`만 `boundary`로 바꾸면 본문 재사용. 대상 함수·픽스처·`pytest.fail` 메시지만 Boundary에 맞게 치환.

이후 본문을 이어간다. GREEN·REFACTOR·assert 본문은 쓰지 않는다.

---

## RED ④ 범위

| 허용 | 금지 |
|------|------|
| `tests/` 아래 스켈레톤·`conftest` 작성·수정 | `src/` **어떤 파일도** 수정·생성 |
| `pytest.fail("RED: {Test ID} — …")` 한 줄 (Then) | `assert` 본문 (상태·dict·줄 ID 검증 등) |
| AAA 주석 — `# Given` / `# When` / `# Then` | `@pytest.mark.skip`, `xfail`, `pass` placeholder |
| `entity.constants` import — **픽스처 데이터만** | 통과 더미 (`assert True`, 빈 `pass` Then) |
| `python -m pytest` 실행·FAIL 확인 | GREEN / REFACTOR 선행 |
| | `git commit` (사용자 요청 전) |
| | Domain·Command **Mock** |

**성공 기준:** 설계표 Test ID마다 스켈레톤이 있고, pytest가 **전부 FAILED** (`pytest.fail` 메시지)여야 RED ④ 완료.

---

## 입력

`/red-skeleton` **만** 실행해도 동작한다. **직전 채팅의 `/red-test-plan` 4블록**을 SSOT로 쓴다. 없으면 `Report/03.REPORT.md` §6.3·기존 T1~T3를 묶음으로 사용.

명령 뒤 텍스트(예: `/red-skeleton D-LOC-01`)가 있으면 **해당 Test ID만** 스켈레톤 작성.

### 설계표에서 가져올 항목

| 항목 | 출처 |
|------|------|
| Test ID | C2C 표 · Track B 표 |
| 함수명 | 테스트 플랜 §3 — `test_{slug}` (Track B·Test ID와 1:1) |
| Given | Rule3 Given — 격자·픽스처 |
| When | Rule3 When — 대상 함수 호출 **주석만** (스켈레톤 단계) |
| Then 메시지 | Track B `Given → Then`·`Expected RED Failure` 요약 |

---

## 상수 · conftest (필수)

### `entity/constants.py` (읽기 전용)

- `src/` 수정 **금지**. 파일이 없으면 `magic-square-tdd` Skill 지침을 따르고, 없으면 보고에 blocker로 명시한다.
- 테스트·conftest에서 **리터럴 34 / 16 / 4 금지** — 아래만 import:

```python
from entity.constants import CELL_MAX, GRID_SIZE, MAGIC
```

- 용도: **픽스처 데이터 구성만** (격자 크기·마법상수·셀 상한). assert·비교에는 쓰지 않는다 (Then에 assert 없음).

### `tests/conftest.py` — `grid_g1`

과제 슬라이드 격자. **빈칸 2개(`0`)**, row-major 좌표 `(row, col)`:

| 좌표 | 값 |
|------|-----|
| `(1, 3)` | `0` |
| `(2, 2)` | `0` |

```python
import pytest

from entity.constants import GRID_SIZE, MAGIC  # noqa: F401 — 픽스처 스코프 문서용

@pytest.fixture
def grid_g1() -> list[list[int]]:
    """4×4 격자 G1 — 빈칸 2개(0), row-major. MAGIC·GRID_SIZE는 entity.constants."""
    return [
        [16, 3, 2, 13],
        [5, 10, 11, 0],
        [9, 6, 0, 12],
        [4, 15, 14, 1],
    ]
```

- `GRID_SIZE`·`MAGIC`는 픽스처 모듈에서 import해 **매직 넘버 대체** (격자 정의 자체는 고정 슬라이드 값).
- 추가 픽스처는 설계표 §3에 있을 때만 같은 파일에 추가.

---

## 스켈레톤 패턴 (필수)

각 테스트 함수:

1. **Given** — `# Given: …` 주석 + Arrange (픽스처 인자 또는 `grid` 준비)
2. **When** — `# When: …` 주석 + **호출 주석 처리** (`# result = validate_lines(grid)`)
3. **Then** — `# Then` + **`pytest.fail` 한 줄만**

```python
import pytest


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given: grid_g1 — 빈칸 2개(0) at (1,3), (2,2) row-major
    grid = grid_g1

    # When: validate_lines(grid) — GREEN(/tdd-red)에서 Act·assert 연결
    # result = validate_lines(grid)

    # Then
    pytest.fail("RED: D-LOC-01 — blank coords row-major not implemented")
```

### Then 규칙

| 항목 | 규칙 |
|------|------|
| 형식 | `pytest.fail("RED: {Test ID} — {Track B Then 요약}")` |
| Test ID | 설계표와 **동일** (예: `T1`, `D-LOC-01`, `VAL-pass`) |
| 개수 | 함수당 **한 줄** |
| 금지 | `assert`, `if`+`fail`, `raise AssertionError`, skip, xfail |

### 함수명 규칙

- `test_{domain}_{seq}_{slug}` — 소문자·언더스코어
- 예: `test_d_loc_01_blank_coords_row_major` ↔ Test ID `D-LOC-01`
- 설계표 §3 함수명이 있으면 **그 이름 우선**

---

## 작업 순서

1. 직전 `/red-test-plan` 4블록(또는 SSOT)에서 Test ID·파일 경로·픽스처를 읽는다.
2. `magic-square-tdd` Skill이 있으면 **자동 따름** (경로·네이밍·상수 import).
3. `tests/conftest.py`에 `grid_g1`이 없으면 추가 (기존 내용 유지).
4. 설계표 Test ID마다 스켈레톤 함수를 **추가** (기존 `/tdd-red` assert 테스트는 **삭제·변환하지 않음** — 별도 묶음이면 새 파일).
5. `python -m pytest tests/ -v` (또는 설계표 §3 경로) 실행.
6. 전 테스트 **FAILED**·메시지에 `RED: {Test ID}` 포함 확인.
7. 아래 보고 형식 제출.

---

## pytest 실행

```bash
python -m pytest tests/ -v
```

또는 설계표에 적힌 경로:

```bash
python -m pytest tests/test_validate_lines.py -v
```

RED ④ 완료 시: **FAILED** = `pytest.fail` 메시지. ERROR(import 실패)는 `entity.constants`·경로 blocker로 보고.

---

## 보고 형식 (필수)

```markdown
Phase: red | Layer: entity | Track: Logic

## 스켈레톤 요약

| Test ID | 함수명 | FAIL 한 줄 |
|---------|--------|------------|
| D-LOC-01 | `test_d_loc_01_blank_coords_row_major` | RED: D-LOC-01 — blank coords row-major not implemented |
| T1 | `test_…` | RED: T1 — … |

## pytest 결과

[N failed — 전부 pytest.fail. 대표 메시지 1~2줄]

## 변경 파일

- `tests/conftest.py` (+N줄) — `grid_g1`
- `tests/test_….py` (+N줄) — 스켈레톤 N건

## 다음 단계

- `/tdd-red` — When의 Act 연결 + assert 본문으로 Then 교체
```

보고 표 **FAIL 한 줄** 열에는 `pytest.fail` 문자열 **그대로** 인용한다.

---

## 세션 3 참고 — T1~T3 스켈레톤 (설계표 있을 때)

| Test ID | 함수명 (예) | pytest.fail 메시지 (예) |
|---------|-------------|-------------------------|
| T1 | `test_t1_pass_all_ten_lines` | `RED: T1 — pass when all ten lines sum to MAGIC` |
| T2 | `test_t2_fail_wrong_line_id_and_sum` | `RED: T2 — fail reports wrong line id and sum` |
| T3 | `test_t3_incomplete_when_zero` | `RED: T3 — incomplete when grid contains zero` |

기존 `tests/test_validate_lines.py`에 **assert RED**가 이미 있으면, 이번 묶음은 **새 파일** 또는 설계표가 지정한 경로에만 스켈레톤 추가.

---

## 금지 사항 (재확인)

- `src/` **수정·생성 금지** (`validate_lines` 구현·`entity/constants.py` 생성 포함)
- **assert 본문**·dict/status 검증 **금지** (④는 스켈레톤만)
- skip·xfail·통과 더미·assert 완화 **금지**
- Then에 `pytest.fail` **외 어떤 검증도** 넣지 않음
- Logic Track: Domain Mock **금지**
- Solver, GridUI, ECB 전체 등 **세션 범위 밖** **금지**
- 한국어로 응답

---

## ARRR 흐름

| 단계 | 커맨드 | 산출 |
|------|--------|------|
| A ③ | `/red-test-plan` | C2C·Track B·플랜 (파일 없음) |
| A ④ | `/red-skeleton` (본 커맨드) | `pytest.fail` 스켈레톤 + conftest |
| R | `/tdd-red` | Act + assert, pytest FAILED |
| R | `/tdd-green` | 최소 구현 |
| R | `/tdd-refactor` | 동작 불변 정리 |

---

## 컨텍스트

- `magic-square-tdd` Skill이 있으면 **자동 따름** (네이밍·경로·상수·픽스처·pytest 명령).
- 명령 뒤 Test ID가 있으면 **그 ID만** 스켈레톤 작성.
- Track A: `Layer: boundary` 선언 후 Boundary 대상·픽스처로 치환.
