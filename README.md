# MagicSquare_XX

4×4 **부분 마방진**의 10선(행·열·대각선) 합이 **34**인지 검증하는 Command와 TDD 루프.

> 상세 요구사항: [docs/PRD.md](docs/PRD.md)

| 항목 | 내용 |
|------|------|
| 버전 | 0.1.0 |
| Python | ≥ 3.10 |
| 상태 | **TDD RED 완료** — `validate_lines` 구현(GREEN) 대기 |

---

## 왜 만드나

부분 마방진을 손으로 채운 뒤 10선을 검증할 때 **대각선을 빼먹어** 시간을 낭비하는 경우가 많다. 이 프로젝트는 한 번의 호출로 10선을 모두 검사하고, 틀리면 **어느 줄인지** 바로 알려 주는 `validate_lines`와 그 계약을 **테스트로 고정**하는 것이 목표다.

- 미완성 격자(`0` 포함)는 `incomplete`로 구분 (R5)
- Solver·GridUI·ECB 전체 앱은 **범위 밖** ([PRD §6.1](docs/PRD.md#61-범위-밖-non-fr))

---

## 빠른 시작

```bash
# 저장소 루트에서
python -m pytest tests/ -v
```

현재 RED 단계: 테스트 3건이 **의도적으로 실패**한다 (`validate_lines` 본문 미구현).

---

## API

```python
from validate_lines import validate_lines

result = validate_lines(grid)
# {
#   "status": "pass" | "fail" | "incomplete",
#   "failed_lines": [{"id": str, "sum": int, "expected": int}, ...],
# }
```

| `status` | 의미 |
|----------|------|
| `pass` | 빈칸 없음, 10선 모두 합 34 |
| `fail` | 빈칸 없음, 하나 이상 합 ≠ 34 — **틀린 줄만** 반환 |
| `incomplete` | `0`이 하나라도 있음 — 합 검증 생략, `failed_lines=[]` |

**줄 ID:** `row:0`~`row:3`, `col:0`~`col:3`, `diag:main`, `diag:anti`

---

## 도메인 요약

| 항목 | 값 |
|------|-----|
| 격자 | 4×4 `list[list[int]]` |
| 셀 | `0`(빈칸) 또는 `1`~`16` |
| MAGIC | `34` |
| 10선 | 행 4 + 열 4 + 주대각 + 부대각 |

---

## 테스트 플랜

SSOT: [docs/PRD.md §7](docs/PRD.md#7-test-requirements--test-id) · Track B (Logic) · AAA — Arrange → Act(`validate_lines`) → Assert(dict)

### FR ↔ Test ID

| FR | 요구사항 (요약) | Test ID |
|----|-----------------|--------|
| FR-1 | 10선×MAGIC 한 번 검증 | T1 (설계) |
| FR-2 | 완성 격자 → `pass` | T1 |
| FR-3 | `0` 포함 → `incomplete` (R5) | T3 |
| FR-4 | 합≠MAGIC → `fail` + 틀린 줄만 | T2, T4~T6 (후보) |
| FR-5 | `failed_lines`에 `id`·`sum`·`expected` | T2 |
| FR-6 | RED→GREEN→REFACTOR 분리 | 전 묶음 |

### RED 묶음 1 — `validate_lines` (구현됨 · assert RED)

| Test ID | FR | 파일 | 함수 | Given | Then (assert) | 상태 |
|---------|-----|------|------|-------|---------------|------|
| **T1** | FR-2 | `tests/test_validate_lines.py` | `test_pass_when_all_ten_lines_sum_to_magic` | `VALID_GRID` (10선 합 34) | `status=="pass"`, `failed_lines==[]` | RED ✅ · GREEN ❌ |
| **T2** | FR-4, FR-5 | 동일 | `test_fail_reports_wrong_line_id_and_sum` | `grid[0][0]=99` | `status=="fail"`, `failed_lines==[{"id":"row:0",…}]` | RED ✅ · GREEN ❌ |
| **T3** | FR-3 | 동일 | `test_incomplete_when_grid_contains_zero` | `grid[0][0]=0` | `status=="incomplete"`, `failed_lines==[]` | RED ✅ · GREEN ❌ |

```bash
# 묶음 1 전체
python -m pytest tests/test_validate_lines.py -v

# 단일 Test ID
python -m pytest tests/test_validate_lines.py::test_pass_when_all_ten_lines_sum_to_magic -v
```

**픽스처:** `VALID_GRID` — 테스트 파일 내 상수. 변형은 `[row[:] for row in VALID_GRID]`로 복사 후 수정.

**현재 pytest:** `3 failed` (의도적) — `validate_lines` 본문 미구현 → `None` 반환.

### RED 후보 — 미구현

| Test ID | 시나리오 | 예정 파일·함수 | 비고 |
|---------|----------|----------------|------|
| **T4** | `diag:main` 실패 보고 | `tests/test_validate_lines.py` | 대각선 누락 방지 (Mom Test E1) |
| **T5** | 복수 `failed_lines` | 동일 | 틀린 줄 여러 개 |
| **T6** | `diag:anti` 실패 | 동일 | 부대각 |
| **D-LOC-01** | `grid_g1` 빈칸 좌표 row-major | `tests/entity/test_d_loc_01.py` · `test_d_loc_01_blank_coords_row_major` | G1 빈칸 `(1,3)`, `(2,2)` 0-index · [§4.4](docs/PRD.md#44-예시-격자-g1-과제-슬라이드) |

```bash
# D-LOC-01 (설계·플랜 완료, 파일 미생성)
python -m pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v
```

**예정 conftest:** `tests/conftest.py` — `grid_g1` (빈칸 2개). `entity.constants`의 `MAGIC`·`GRID_SIZE` import만.

### Golden Master (선택 · post-GREEN)

| 항목 | 규격 |
|------|------|
| 헬퍼 | `tests/_approval.py` — `assert_matches_golden` |
| baseline | `tests/golden/{id}.approved.txt` |
| 갱신 | `UPDATE_GOLDEN=1` pytest **만** |
| 포맷 | 3행: `status=` / `int6=` (6개, **1-index**) / `codes=` (`INC:zero`, `LINE:{id}`) |

```powershell
$env:UPDATE_GOLDEN=1; python -m pytest tests/ -v
Remove-Item Env:UPDATE_GOLDEN -ErrorAction SilentlyContinue
python -m pytest tests/ -v
```

### 성공 기준 (Acceptance)

| # | 기준 | 증거 Test ID | 현재 |
|---|------|--------------|------|
| AC-1 | 10선×34 Command | T1 | RED ✅ / GREEN ❌ |
| AC-2 | pass / fail / incomplete | T1~T3 | RED ✅ |
| AC-3 | `failed_lines` id·sum·expected | T2 | RED ✅ |
| AC-4 | `pytest tests/ -v` 전부 PASS | — | ❌ |
| AC-5 | (선택) golden matched | T1+ | ❌ |

### TDD 묶음 순서 (PRD §15)

| 순서 | RED 묶음 | Command |
|------|----------|---------|
| 1 | T1~T3 GREEN | `/green-minimal` |
| 2 | Golden (선택) | `/golden-master` |
| 3 | REFACTOR | `/refactor-smell` → `/refactor-safe` |
| 4 | T4~T6, D-LOC-01 | `/red-test-plan` → `/red-skeleton` → … |

---

## TDD · Cursor 워크플로 (ARRR)

```
/red-test-plan → /red-skeleton → /tdd-red
  → /green-minimal → /golden-master
  → /refactor-smell → /refactor-safe
```

| 리소스 | 경로 |
|--------|------|
| 프로젝트 규칙 | `.cursorrules` |
| TDD Skill | `.cursor/skills/magic-square-tdd/SKILL.md` |
| Docs Export Skill | `.cursor/skills/magic-square-docs/SKILL.md` |
| 세션 Export | `/export-session` |

---

## 프로젝트 구조

```
MagicSquare_XX/
├── docs/PRD.md                    # 요구사항·테스트 SSOT
├── src/validate_lines.py          # Command (GREEN 대기)
├── tests/
│   ├── test_validate_lines.py     # T1~T3 (RED)
│   ├── conftest.py                # grid_g1 (D-LOC-01 예정)
│   └── entity/test_d_loc_01.py    # D-LOC-01 (예정)
├── .cursor/commands/
├── .cursor/skills/
├── Report/
└── Prompting/
```

---

## 다음 단계

1. `/green-minimal` — `validate_lines` 최소 구현
2. (선택) `/golden-master` — approval baseline
3. `/refactor-smell` → `/refactor-safe` — 동작 불변 리팩터

전체 로드맵: [PRD §15](docs/PRD.md#15-로드맵)

---

## 세션 문서

| NN | Report | Transcript | Phase | 주제 |
|----|--------|------------|-------|------|
| 01 | [Report/01.REPORT.md](Report/01.REPORT.md) | [Prompting/01.Export-Transcript.md](Prompting/01.Export-Transcript.md) | — | Mom Test 인터뷰 |
| 02 | [Report/02.MomTest-Questions_REPORT.md](Report/02.MomTest-Questions_REPORT.md) | [Prompting/02.MomTest-Questions-Prompt.md](Prompting/02.MomTest-Questions-Prompt.md) | — | Mom Test 질문 |
| 03 | [Report/03.REPORT.md](Report/03.REPORT.md) | [Prompting/03.Session3-Workbook-Prompt.md](Prompting/03.Session3-Workbook-Prompt.md) | — | 세션 3 워크북 |
| 04 | [Report/04.Harness-TDD-RED_REPORT.md](Report/04.Harness-TDD-RED_REPORT.md) | [Prompting/04.Export-Transcript.md](Prompting/04.Export-Transcript.md) | RED | Harness · TDD RED |
| 05 | [Report/05.Export-Session_REPORT.md](Report/05.Export-Session_REPORT.md) | [Prompting/05.Export-Transcript.md](Prompting/05.Export-Transcript.md) | — | Export Session |

---

## 관련 문서

| 문서 | 설명 |
|------|------|
| [docs/PRD.md](docs/PRD.md) | FR, Test ID, API, ARRR, 구현 상태 |
| [Report/03.REPORT.md](Report/03.REPORT.md) | Mom Test · R-G-I-O · 성공 기준 |
| [Report/04.Harness-TDD-RED_REPORT.md](Report/04.Harness-TDD-RED_REPORT.md) | Harness · RED 상세 |
