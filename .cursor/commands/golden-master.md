# Golden Master — Approval Test 구축·검증

MagicSquare_XX **GREEN PASS 이후** — 대상 Test ID에 **Golden Master(Approval Test)** 를 연결·생성·검증한다.
기준 파일은 **실행 결과로만** 갱신한다. 수동 편집으로 통과 우회 **금지**.

선행: `/green-minimal` (또는 동등 GREEN) — **대상 Test ID pytest PASS**.
SSOT: 직전 GREEN 묶음·Test ID, `.cursorrules`, `entity/constants.py`.
**Skill:** `magic-square-tdd` Skill이 있으면 자동 따름.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 작성:

```
Phase: green | Layer: entity | Track: Logic
```

- `Layer`: `entity` (기본) 또는 `boundary` (Track A — 선언만 치환)
- `Track`: `Logic` (기본) 또는 `UI`

이후 본문을 이어간다.

---

## 전제 (필수)

| 항목 | 조건 |
|------|------|
| 대상 Test ID | `/green-minimal`·`/tdd-red`로 **이미 PASS** |
| 단위 테스트 | 해당 함수 `python -m pytest …::test_…` **PASS** 확인 후에만 golden 작업 |
| 미충족 시 | golden 생성 **중단** — GREEN 먼저 완료 보고 |

명령 뒤 텍스트(예: `/golden-master T1`)가 있으면 **그 Test ID만** 처리. 없으면 직전 GREEN 묶음 전체.

---

## Golden Master 범위

| 허용 | 금지 |
|------|------|
| `tests/_approval.py` 생성·`assert_matches_golden` 추가 | `tests/golden/*.approved.txt` **수동 편집** |
| `tests/golden/{id}.approved.txt` — `UPDATE_GOLDEN=1`로만 생성·갱신 | golden 내용을 손으로 맞춰 matched 우회 |
| 대상 테스트에 approval 호출 연결 | PASS 안 된 Test ID에 golden 생성 |
| `UPDATE_GOLDEN` 없이 matched 검증 | assert 완화·skip·xfail |
| | `src/` 변경 (canonical 출력이 이미 PASS인 전제) |
| | `git commit` (사용자 요청 전) |

**성공 기준:** `UPDATE_GOLDEN` 없이 pytest 시 **matched** (golden ≡ 실제 canonical 출력).

---

## 절차 (필수 순서)

### 1. `tests/_approval.py` — `assert_matches_golden`

파일이 없으면 생성. 핵심 계약:

```python
"""Approval test helpers — golden file compare only."""

from __future__ import annotations

import os
from pathlib import Path

GOLDEN_DIR = Path(__file__).resolve().parent / "golden"


def assert_matches_golden(
    test_id: str,
    actual: str,
    *,
    update: bool | None = None,
) -> None:
    """Compare *actual* to tests/golden/{id}.approved.txt.

    Set update=True or env UPDATE_GOLDEN=1 to write/overwrite golden.
    """
    if update is None:
        update = os.environ.get("UPDATE_GOLDEN") == "1"

    golden_path = GOLDEN_DIR / f"{_slug(test_id)}.approved.txt"
    golden_path.parent.mkdir(parents=True, exist_ok=True)

    if update:
        golden_path.write_text(actual, encoding="utf-8")
        return

    if not golden_path.is_file():
        raise AssertionError(f"golden missing: {golden_path}")

    expected = golden_path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(
            f"golden mismatch: {golden_path}\n--- expected ---\n{expected}--- actual ---\n{actual}"
        )


def _slug(test_id: str) -> str:
    return test_id.strip().lower().replace("_", "-")
```

- 비교는 **문자열 전체 일치** (정규화는 `canonicalize_approval`에서만).
- diff는 `AssertionError` 메시지로 보고.

### 2. `tests/golden/{id}.approved.txt` 연결

| 항목 | 규칙 |
|------|------|
| 경로 | `tests/golden/{id}.approved.txt` |
| `{id}` | Test ID slug — `T1`→`t1`, `D-LOC-01`→`d-loc-01` |
| 연결 | 대상 테스트 Then에서 `canonicalize_approval(...)` → `assert_matches_golden(test_id, text)` |
| 인코딩 | UTF-8, LF, 파일 끝 개행 1개 |

**테스트 연결 예:**

```python
from _approval import assert_matches_golden, canonicalize_approval

def test_t1_pass_all_ten_lines():
    # Given / When … (기존 GREEN assert 유지 가능)
    result = validate_lines(grid)
    # Approval (golden)
    assert_matches_golden("T1", canonicalize_approval(result, grid=grid))
```

- 기존 unit assert와 approval은 **공존** 가능. approval은 회귀 스냅샷 역할.

### 3. `UPDATE_GOLDEN=1` — 기준 파일 생성

대상 Test ID가 PASS인 상태에서 **한 번** 실행:

**PowerShell:**

```powershell
$env:UPDATE_GOLDEN=1; python -m pytest tests/test_validate_lines.py::test_t1_pass_all_ten_lines -v
```

**bash / sh:**

```bash
UPDATE_GOLDEN=1 python -m pytest tests/test_validate_lines.py::test_t1_pass_all_ten_lines -v
```

- golden 파일은 이 실행의 `canonicalize_approval` 출력으로 **자동 기록**.
- 생성 후 `git diff tests/golden/`로 내용 검토 (수정하지 않음).

### 4. `UPDATE_GOLDEN` 없이 matched 확인

환경 변수 **제거·미설정** 후 동일 테스트 재실행:

```bash
python -m pytest tests/test_validate_lines.py::test_t1_pass_all_ten_lines -v
```

- **PASS** = matched.
- **FAIL** = mismatch — `src/` 또는 canonical 로직 수정. golden **수동 수정 금지**.

---

## Golden 포맷 (고정)

`.approved.txt` 본문은 **아래 3행 고정**. `canonicalize_approval`만 이 형식을 생성한다.

```
status=<pass|fail|incomplete>
int6=<i1>,<i2>,<i3>,<i4>,<i5>,<i6>
codes=<token>|<token>|…
```

| 필드 | 규칙 |
|------|------|
| `status` | `validate_lines` 반환 `status` 그대로 |
| `int6` | **정확히 6개** 정수, 쉼표 구분, **1-index** 좌표 규칙 |
| `codes` | 에러·줄 코드 문자열, `\|` 구분; 없으면 `codes=` (빈) |

### `int6` — 1-index 규칙

| 슬롯 | 의미 |
|------|------|
| `i1`,`i2` | 첫 번째 `0`(빈칸) `(row,col)` — **1-index** (`1`~`GRID_SIZE`) |
| `i3`,`i4` | 두 번째 `0` `(row,col)` — **1-index**; 빈칸 1개면 `0,0` |
| `i5`,`i6` | 예약 — 완성 격자·pass: `0,0`; fail 시 첫 `failed_lines[0].sum`·`MAGIC` 등 설계표 invariant |

- **0-index 금지** — golden에는 `1`~`4`만 좌표로 등장.
- 예: `grid_g1` 빈칸 0-index `(1,3)`, `(2,2)` → `int6=2,4,3,3,0,0`

### `codes` — 에러 코드 문자열 (고정)

| 상황 | `codes` 값 |
|------|------------|
| `pass` | `codes=` (빈) |
| `incomplete` | `codes=INC:zero` |
| `fail` (줄 1개) | `codes=LINE:{id}` — `{id}` = `row:0`·`diag:main` 등 **줄 ID 그대로** |
| `fail` (줄 여러 개) | `codes=LINE:{id}|LINE:{id}|…` — **정렬 고정** (row → col → diag:main → diag:anti) |

- 토큰 형식: `PREFIX:payload` (`INC`, `LINE` 만 사용 — **E001~E005 사용 금지**).
- 공백·대소문자 변경 **금지**.

### `canonicalize_approval` (같은 `_approval.py`에 추가)

```python
from entity.constants import GRID_SIZE, MAGIC


def canonicalize_approval(result: dict, *, grid: list[list[int]] | None = None) -> str:
    status = result["status"]
    int6 = _blank_int6(grid or [], result)
    codes = _codes_line(result)
    return f"status={status}\nint6={int6}\ncodes={codes}\n"
```

- 구현 세부는 Test ID invariant에 맞게 최소 작성. **포맷 3행은 불변**.

---

## 작업 순서 (체크리스트)

1. 대상 Test ID unit pytest **PASS** 재확인
2. `tests/_approval.py` 없으면 생성 (`assert_matches_golden`, `canonicalize_approval`)
3. 대상 테스트에 golden 연결
4. `UPDATE_GOLDEN=1` pytest → `tests/golden/{id}.approved.txt` 생성
5. `UPDATE_GOLDEN` 해제 후 pytest → **matched** 확인
6. mismatch 시 golden 수정 없이 `canonicalize_approval`·`src/` 조정
7. 보고 형식 제출

---

## 보고 형식 (필수)

```markdown
Phase: green | Layer: entity | Track: Logic

## Golden Master

| Test ID | golden 경로 | matched |
|---------|-------------|---------|
| T1 | `tests/golden/t1.approved.txt` | ✅ matched |
| T2 | `tests/golden/t2.approved.txt` | ❌ mismatch |

## diff 요약

- [matched] — (생략)
- [mismatch] — `status=` 동일 / `int6` 3번째 값 `3`→`4` / `codes` `LINE:row:0` 누락 등 1~3줄

## 변경 파일

- `tests/_approval.py` (신규 또는 +N줄)
- `tests/golden/{id}.approved.txt` (UPDATE_GOLDEN=1로 생성)
- `tests/test_….py` — approval 호출 (+N줄)

## pytest

- 생성: `UPDATE_GOLDEN=1 pytest …::test_…` → PASS
- 검증: `pytest …::test_…` (UPDATE_GOLDEN 없음) → PASS = matched

## 다음 단계

- 다음 Test ID golden 또는 다음 RED 묶음
- commit: 사용자 요청 시 — `golden: {Test ID} approval baseline`
```

---

## 금지 사항 (재확인)

- `tests/golden/*.approved.txt` **수동 편집**으로 matched 맞추기 **금지**
- PASS되지 않은 Test ID에 golden baseline 생성 **금지**
- Golden 포맷 (`status` / `int6` / `codes`) 임의 변경 **금지**
- `int6`에 0-index 좌표 넣기 **금지**
- E001~E005 코드 문자열 사용 **금지**
- assert 완화·skip·xfail **금지**
- 한국어로 응답

---

## ARRR · TDD 위치

| 단계 | 커맨드 | 산출 |
|------|--------|------|
| GREEN | `/green-minimal` | unit PASS |
| **Golden** | **`/golden-master`** (본 커맨드) | approval baseline + matched |
| R | `/tdd-refactor` | 동작·golden 불변 전제 정리 |

---

## 컨텍스트

- Approval test는 **회귀 스냅샷** — 기능 변경 시 `UPDATE_GOLDEN=1`로만 baseline 갱신.
- 명령 뒤 Test ID 없으면 직전 GREEN 묶음 **순차** 처리.
- Track A(boundary): `Layer: boundary`, `canonicalize_approval`·`codes`를 Boundary 출력 규격으로 치환.
