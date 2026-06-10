---
name: magic-square-tdd
description: >-
  MagicSquare_XX ARRR·Dual-Track TDD workflow (C2C, pytest.fail skeleton,
  golden master, safe refactor). Use when Phase is red, green, or refactor;
  when running Commands /red-test-plan, /red-skeleton, /green-minimal,
  /refactor-safe; or when the user mentions TDD, RED, GREEN, REFACTOR,
  Dual-Track, C2C, or pytest.fail. SSOT: .cursorrules, docs/PRD.md.
disable-model-invocation: true
---

# MagicSquare TDD

MagicSquare_XX 4×4 부분 마방진 — **ARRR + Dual-Track TDD**. 한국어 응답.
SSOT: `.cursorrules`, `docs/PRD.md` (없으면 `Report/03.REPORT.md`).

---

## 1. ARRR ↔ TDD 매핑

| ARRR | TDD | Command | 산출 |
|------|-----|---------|------|
| **Ask** | RED ③④ | `/red-test-plan`, `/red-skeleton` | C2C·플랜·`pytest.fail` 스켈레톤 |
| **Ask** | RED (assert) | `/tdd-red` | 실패 assert |
| **Respond** | GREEN | `/green-minimal` | 최소 구현·PASS |
| **Respond** | Golden | `/golden-master` | approval baseline |
| **Refine** ⑦ | REFACTOR smell | `/refactor-smell` | 스멜 표 (수정 없음) |
| **Refine** | REFACTOR safe | `/refactor-safe` | Budget 내 1스멜 |

순서: **RED → GREEN → (Golden) → REFACTOR**. 단계 건너뛰기 금지.

---

## 2. Phase 선언 (응답 첫 줄)

| 단계 | 형식 |
|------|------|
| RED 설계 | `Phase: red \| Layer: entity \| Track: Logic` |
| RED 스켈레톤 | `Phase: red \| Layer: entity \| Track: Logic` |
| GREEN | `Phase: green \| Layer: entity \| Track: Logic` |
| Golden | `Phase: green \| Layer: entity \| Track: Logic` |
| REFACTOR smell | `Phase: refactor \| Scope: src/ tests/ \| Track: Logic+UI` |
| REFACTOR safe | `Phase: refactor \| Layer: entity \| Track: Logic` |

- `Layer`: `entity` (Track B) 또는 `boundary` (Track A)
- `Track`: `Logic` 또는 `UI`
- Track A: 본문 재사용, **선언의 `Layer`만 `boundary`로 치환**

---

## 3. C2C (Command-to-Contract) Rule 1~3

| Rule | 내용 |
|------|------|
| **Rule1** | PRD FR **원문 인용** (또는 SSOT 동등 문장) |
| **Rule2** | FR → **To-Do 1개** (검증 가능한 단일 행동) |
| **Rule3** | **Test ID** + **Given / When / Then** (AAA) |

- Given = Arrange (`grid`, 픽스처)
- When = Act (`validate_lines(grid)` 1회)
- Then = Assert (반환 dict) 또는 RED ④ `pytest.fail` 1줄

---

## 4. RED 절대 금지

| 금지 | 적용 단계 |
|------|-----------|
| `src/` 수정·생성 | ③ `/red-test-plan`, ④ `/red-skeleton`, `/tdd-red` |
| `@pytest.mark.skip`, `xfail`, `pass` placeholder | 전 RED |
| assert 완화·삭제 | 전 RED |
| Logic Track **Domain Mock** | 전 RED |
| E001~E005 emit | 전 RED |
| GREEN/REFACTOR 선행 | RED 중 |
| `git commit` (사용자 요청 전) | 전체 |

**RED ③** (`/red-test-plan`): 파일 생성 없음 — 표·플랜만.
**RED ④** (`/red-skeleton`): Then = `pytest.fail("RED: {Test ID} — …")` **한 줄만** — assert 본문 금지.

---

## 5. GREEN 규칙

- **1커밋 = 1 RED 묶음** — 여러 묶음 동시 GREEN 금지
- **이번 묶음 Test ID만** PASS — 묶음 외는 FAIL 유지
- `pytest.fail` 제거 → Act + assert 교체
- 상수 SSOT — 리터럴 `34`/`16`/`4` 금지:

```python
from entity.constants import CELL_MAX, GRID_SIZE, MAGIC
```

- E001~E005 raise/return 금지
- entity → boundary/control import 금지
- REFACTOR·기능 추가·버그 수정 금지 (별도 단계)
- `git commit` — 사용자 요청 시만

### API 계약

```python
validate_lines(grid) -> {"status": "pass"|"fail"|"incomplete", "failed_lines": [...]}
```

- R5: `0` 포함 → `incomplete`, `failed_lines=[]`
- fail: 틀린 줄만 `{id, sum, expected: MAGIC}`
- 줄 ID: `row:0`~`row:3`, `col:0`~`col:3`, `diag:main`, `diag:anti`

---

## 6. REFACTOR 규칙

### `/refactor-smell` (탐지만)

- 전제: `python -m pytest tests/ -v` **전부 PASS** — 아니면 중단
- **수정·commit 금지**
- 스멜: Long Method · Duplicated Code · Mysterious Name · Magic Number · ECB 위반 · Feature Envy
- P0 > P1 > P2 — 후보 1~3개 → `/refactor-safe`에 넘김

### `/refactor-safe` (1스멜만)

**Change Budget (1회):** 파일 ≤3 · 클래스 ≤1 · 메서드 ≤3

| 불변 (golden 유지) | 금지 |
|-------------------|------|
| 입출력·예외 | 기능 추가·버그 수정 |
| `int6` 1-index 좌표 규칙 | assert 완화 |
| golden `codes` 포맷 (`INC:`, `LINE:`) | golden 수동 편집 |
| observable 동작 | E001~E005 emit |

**완료 검증:** `pytest tests/ -v` PASS + golden **matched** (`UPDATE_GOLDEN` 없음).

**golden diff:**

| 종류 | 조치 |
|------|------|
| 없음 | 완료 |
| 의도적 | ISS 문서화 → `UPDATE_GOLDEN=1` → 재검증 |
| 비의도 | **롤백** |

---

## 7. Track A (UI) vs Track B (Logic)

| 항목 | Track B — Logic | Track A — UI (Boundary) |
|------|-----------------|-------------------------|
| Layer | `entity` | `boundary` |
| 대상 | `validate_lines`, 도메인 dict | ResultDisplay·표시 계약 |
| 테스트 | 반환 dict **직접 assert** | Boundary 출력·포맷 |
| Mock | **Domain Mock 금지** | Boundary Mock 허용 (UI 세션) |
| C2C | Command·Rule | 표시·에러 표현 |
| 전환 | 기본 | 선언 `Layer: boundary`만 치환 |

세션 3 기본: **Track B · Logic · entity**.

---

## 8. Command 체인

```
/red-test-plan     → C2C·Track B·플랜 (파일 없음)
       ↓
/red-skeleton      → pytest.fail 스켈레톤 + conftest grid_g1
       ↓
/tdd-red           → Act + assert (FAILED)
       ↓
/green-minimal     → src 최소 구현 (PASS, 1묶음)
       ↓
/golden-master     → tests/golden/{id}.approved.txt (선택)
       ↓
/refactor-smell    → 스멜 표 (수정 없음)
       ↓
/refactor-safe     → 스멜 1개 safe (Budget)
```

각 Command 상세: `.cursor/commands/{name}.md` — **명시 호출 시 해당 파일 우선**.

---

## 9. pytest 명령 패턴

```bash
# 전체
python -m pytest tests/ -v

# 단일 테스트
python -m pytest tests/test_validate_lines.py::test_t1_pass_all_ten_lines -v

# 파일
python -m pytest tests/test_validate_lines.py -v
```

**Golden baseline 생성 (PowerShell):**

```powershell
$env:UPDATE_GOLDEN=1; python -m pytest tests/ -v
Remove-Item Env:UPDATE_GOLDEN -ErrorAction SilentlyContinue
python -m pytest tests/ -v
```

**Golden 검증:** `UPDATE_GOLDEN` **미설정** — matched = PASS.

`pyproject.toml`: `testpaths = ["tests"]`, `pythonpath = ["src"]`.

---

## 10. 완료 보고 형식

### RED ③ `/red-test-plan`

4블록: ① C2C ② Track B ③ 테스트 플랜 ④ ECB·Mock 점검 → `/red-skeleton 으로 넘길 준비됐다`

### RED ④ `/red-skeleton`

| Test ID | 함수명 | FAIL 한 줄 | 변경 파일 (`tests/`만) |

### GREEN `/green-minimal`

| PASS Test ID | 변경 파일 (`src/`·`tests/`) | pytest N passed |

### Golden `/golden-master`

| Test ID | golden 경로 | matched | diff 요약 |

### REFACTOR smell

스멜 표 (P/유형/위치) + `/refactor-safe` 후보 1~3 — **P0 1개** 선택 안내

### REFACTOR safe

선택 스멜 · 변경 요약 · pytest · golden matched · Budget 실제 소비

---

## 도메인 · 픽스처 · Golden (고정)

| 항목 | 값 |
|------|-----|
| 격자 | 4×4, `0` 또는 1~16 |
| 10선 | 행4+열4+대각2, 합 `MAGIC` |
| `grid_g1` | 빈칸 `(1,3)`, `(2,2)` 0-index — conftest |
| golden 3행 | `status=` / `int6=` (6개, **1-index**) / `codes=` |
| codes | `INC:zero`, `LINE:{id}` — E001~E005 금지 |

### 스켈레톤 Then (RED ④)

```python
pytest.fail("RED: {Test ID} — {요약}")
```

### AAA 주석

```python
# Given: …
# When: …
# Then
```

---

## ECB · 범위 밖

- **만들지 않음:** Solver, GridUI, ECB 전체 앱, 1~16 중복 검증
- **테스트:** `tests/test_validate_lines.py`, `tests/_approval.py`, `tests/conftest.py`
- **구현:** `src/validate_lines.py`, `src/entity/constants.py`
- **응답:** 한국어 · 변경은 요청·Command 범위만 · `git commit` 사용자 요청 시만

---

## Quick checklist

```
RED ③:  src/ untouched?  4 blocks done?
RED ④:  pytest.fail only?  grid_g1?  constants import?
GREEN:  one bundle?  MAGIC not literal?  bundle PASS only?
GOLDEN: UPDATE_GOLDEN off → matched?
SMELL:  all PASS first?  no edits?
SAFE:   one smell?  Budget OK?  rollback if unintended golden diff?
```
