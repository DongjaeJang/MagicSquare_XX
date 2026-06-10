# GREEN Minimal — ARRR R단계 (Respond = GREEN)

MagicSquare_XX **GREEN 전용** — **RED 1묶음**당 `src/` **최소 구현**으로 해당 Test ID만 PASS시킨다.
**1커밋 = 1 RED 묶음** 원칙. `git commit`은 사용자가 명시 요청할 때만.

선행: `/red-test-plan` → `/red-skeleton` → `/tdd-red` (또는 동등 RED 확정).
SSOT: 직전 RED 묶음·C2C·Track B, `.cursorrules`, `entity/constants.py`.
**Skill:** `magic-square-tdd` Skill이 있으면 자동 따름.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 작성:

```
Phase: green | Layer: entity | Track: Logic
```

- `Layer`: `entity` (기본) 또는 `boundary` (Track A — 선언만 치환)
- `Track`: `Logic` (기본) 또는 `UI`

이후 본문을 이어간다. REFACTOR·다음 RED 묶음 선행 해결은 쓰지 않는다.

---

## GREEN 범위

| 허용 | 금지 |
|------|------|
| **이번 RED 묶음** Test ID를 PASS시키는 `src/` 최소 구현 | 이번 묶음 **외** Test ID 동시 해결 |
| `tests/` — `pytest.fail` 제거·Act 연결·assert 교체 | assert 완화·삭제·조건 느슨화 |
| `entity/constants.py` 참조 (매직넘버 대체) | 리터럴 `34` / `16` / `4` 하드코딩 |
| 회귀 실패 시 **즉시** 최소 수정 | REFACTOR (구조 정리·이름 변경·중복 제거) |
| `python -m pytest` PASS 확인 | `@pytest.mark.skip`, `xfail`, `pass` placeholder |
| | E001~E005 `raise` / `return` |
| | entity → boundary·control **import** |
| | Solver, GridUI, ECB 전체 등 세션 범위 밖 |
| | `git commit` (사용자 요청 전) |

**성공 기준:** 이번 묶음 Test ID **전부 PASS**, 묶음 외 RED·스켈레톤은 **그대로 FAIL** 유지.

---

## 입력

`/green-minimal` **만** 실행해도 동작한다. **직전 RED 묶음** Test ID 목록을 채팅·`/red-test-plan` §RED 묶음에서 자동 추출.

명령 뒤 텍스트(예: `/green-minimal T1`)가 있으면 **그 Test ID가 속한 묶음**만 GREEN (단일 ID 지정 시에도 묶음 단위 원칙 유지 — 묶음에 ID 1개뿐이면 1개만).

---

## 절차 (필수 순서)

### 1. RED 재확인

- 이번 묶음 Test ID·함수명·Track B `Given → Then`을 나열한다.
- `python -m pytest`로 해당 ID가 **FAILED**(`pytest.fail` 또는 assert 실패)인지 확인한다.
- 묶음 외 테스트는 건드리지 않는다.

### 2. `src/` 최소 구현

- **이번 묶음을 PASS시키는 최소 코드만** 추가·수정한다.
- YAGNI: 다음 묶음·REFACTOR를 위한 선행 구현 **금지**.
- 상수는 **`entity/constants.py` SSOT**만 사용:

```python
from entity.constants import CELL_MAX, GRID_SIZE, MAGIC
```

- `expected` 필드·비교에는 `MAGIC` 사용. 격자 차원·반복에는 `GRID_SIZE`. 셀 상한 문서화에 `CELL_MAX`.

### 3. `pytest.fail` 제거 · assert 교체

- 스켈레톤 `# When` 주석을 해제: `result = validate_lines(grid)` (또는 설계표 대상 함수).
- `# Then`의 `pytest.fail(...)` **삭제** → Track B·`/tdd-red` 계약에 맞는 **assert 본문**으로 교체.
- AAA 주석(`# Given` / `# When` / `# Then`) 유지.

### 4. PASS 확인

- 단일 테스트 → 파일 전체 순으로 pytest 실행 (아래 명령).
- 이번 묶음 **전부 PASS** 확인.
- **회귀:** 묶음 외가 깨지면 assert 완화 없이 `src/` 또는 테스트를 **즉시** 최소 수정.

---

## API 계약 (assert SSOT)

```python
result = {
    "status": "pass" | "fail" | "incomplete",
    "failed_lines": [{"id": str, "sum": int, "expected": int}, ...],
}
```

| status | 조건 | failed_lines |
|--------|------|--------------|
| `pass` | 10선 모두 합 `MAGIC` | `[]` |
| `fail` | `0` 없음, 하나 이상 합 ≠ `MAGIC` | **틀린 줄만** |
| `incomplete` | `0` 하나라도 (R5) | `[]` |

- 줄 ID: `row:0`~`row:3`, `col:0`~`col:3`, `diag:main`, `diag:anti`
- `expected`는 항상 `MAGIC` (`entity.constants`)

---

## ECB · 상수 규칙

| 항목 | 규칙 |
|------|------|
| `entity/constants.py` | `MAGIC`, `GRID_SIZE`, `CELL_MAX` SSOT — **유일한** 34/16/4 출처 |
| entity 코드 | `boundary`·`control` 패키지 **import 금지** |
| E001~E005 | **raise·return 금지** — 오류코드 emit 없음 |
| Command | 세션 3: `validate_lines` — entity 계층 내 최소 구현 (Boundary 없음) |

---

## pytest 명령 (예시 2개)

**단일 테스트** (이번 묶음 1 Test ID):

```bash
python -m pytest tests/test_validate_lines.py::test_t1_pass_all_ten_lines -v
```

**파일 전체** (회귀·묶음 전체 확인):

```bash
python -m pytest tests/test_validate_lines.py -v
```

- 묶음이 다른 파일이면 설계표 §3 경로로 치환.
- PASS 기준: 지정 단일 테스트 PASS → 파일 전체에서 **이번 묶음 PASS + 묶음 외 기존 상태 유지**.

---

## 작업 순서 (체크리스트)

1. RED 묶음 Test ID 확정·pytest FAIL 재확인
2. `magic-square-tdd` Skill 있으면 자동 따름
3. `entity/constants.py` 없으면 **최소 상수만** 추가 (묶음 범위 내)
4. `src/` 최소 구현 (묶음 Test ID만 통과)
5. `tests/` — 해당 함수만 `pytest.fail` → assert 교체
6. 단일 테스트 pytest → 파일 전체 pytest
7. 회귀 실패 시 즉시 수정 (assert 완화 금지)
8. 보고 형식 제출
9. `git commit` — **사용자 요청 시만**, 메시지에 RED 묶음·Test ID 명시

---

## 보고 형식 (필수)

```markdown
Phase: green | Layer: entity | Track: Logic

## PASS Test ID

| Test ID | 함수명 | 판정 |
|---------|--------|------|
| T1 | `test_t1_pass_all_ten_lines` | PASS |
| T2 | `test_t2_fail_wrong_line_id_and_sum` | PASS |

- RED 묶음: [T1, T2, …]
- 묶음 외: [여전히 FAIL/스켈레톤인 ID 목록]

## 변경 파일

| 파일 | 변경 요약 |
|------|-----------|
| `src/entity/constants.py` | MAGIC, GRID_SIZE, CELL_MAX (없을 때만) |
| `src/validate_lines.py` | 묶음 최소 구현 (+N줄) |
| `tests/test_validate_lines.py` | pytest.fail → assert (+N줄) |

## pytest 결과

[단일: N passed · 파일 전체: M passed, K failed — 회귀 없음 / 회귀 수정 내역 1줄]

## 회귀 처리

- [없음] 또는 [깨진 Test ID · 원인 · 최소 수정 한 줄]

## 다음 단계

- 다음 RED 묶음: `/red-test-plan` 또는 `/tdd-red`
- REFACTOR: 사용자 요청 또는 별도 커맨드 (본 GREEN에서 하지 않음)
- commit: 사용자 요청 시 — `GREEN: {묶음명} — {Test ID 목록}`
```

---

## assert 교체 예시 (T1)

**Before (스켈레톤):**

```python
    # When: validate_lines(grid) — GREEN(/tdd-red)에서 Act·assert 연결
    # result = validate_lines(grid)

    # Then
    pytest.fail("RED: T1 — pass when all ten lines sum to MAGIC")
```

**After (본 커맨드):**

```python
from entity.constants import MAGIC
from validate_lines import validate_lines

    # When
    result = validate_lines(grid)

    # Then
    assert result["status"] == "pass"
    assert result["failed_lines"] == []
```

---

## 금지 사항 (재확인)

- 이번 RED 묶음 **외** ID를 한 번에 GREEN하려는 구현 **금지**
- REFACTOR (리네임·추출·최적화) **금지** — 동작만 맞춘다
- assert 완화·skip·xfail로 PASS 우회 **금지**
- 하드코딩 `34`/`16`/`4` — `entity.constants` 없이 쓰지 않음
- E001~E005 emit **금지**
- entity가 boundary/control을 import **금지**
- 한국어로 응답

---

## ARRR 흐름

| 단계 | 커맨드 | 산출 |
|------|--------|------|
| A ③ | `/red-test-plan` | C2C·플랜 |
| A ④ | `/red-skeleton` | `pytest.fail` 스켈레톤 |
| R | `/tdd-red` | assert RED |
| **R** | **`/green-minimal`** (본 커맨드) | **최소 구현 + PASS** |
| R | `/tdd-refactor` | 동작 불변 정리 (별도) |

---

## 컨텍스트

- **1커밋 = 1 RED 묶음** — 여러 묶음을 한 GREEN·한 커밋에 넣지 않는다.
- 명령 뒤 Test ID가 있어도 **묶음 단위**로만 `src/`를 확장한다.
- Track A: `Layer: boundary` 선언 후 Boundary 구현·assert로 치환.
