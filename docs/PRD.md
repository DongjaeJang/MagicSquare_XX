# MagicSquare_XX — Product Requirements Document (PRD)

| 항목 | 내용 |
|------|------|
| 프로젝트 | `MagicSquare_XX` |
| 버전 | 0.1.0 |
| 문서 버전 | 1.0 |
| 작성일 | 2026-06-10 |
| 상태 | 세션 3 — **TDD RED 완료**, GREEN 대기 |
| SSOT 우선순위 | 본 PRD → `.cursorrules` → `Report/03.REPORT.md` |

---

## 1. 주제 (한 문장)

4×4 부분 마방진에서 빈칸을 채운 직후, 행·열·대각선 **10선**이 각각 **34**인지 빠르게 확정하고, 틀리면 **어느 줄인지** 바로 짚을 수 있게 **검증 규칙(Command)** 과 **테스트 루프**를 만든다. 미완성 격자(`0` 포함)는 `incomplete`로 구분한다.

---

## 2. 배경 · Mom Test

### 2.1 페르소나

| 항목 | 내용 |
|------|------|
| 역할 | 4×4 **부분** 마방진 학습자 |
| 행동 | 손풀이 / 코드로 10선 검증 |
| 도메인 | 4×4 격자, 빈칸 2개(`?` 또는 `0`), 셀 값 1~16, 10선 각 합 34 |

### 2.2 진짜 문제

4×4 부분 마방진(`?` 2칸)을 손으로 채운 뒤 10선 합 34를 확인할 때 **대각선을 까먹어** 약 **20분**을 쓰고, 다 채운 뒤에야 틀렸다는 걸 알며, `?` 두 칸만 고친 뒤 10선 전부를 다시 검증한다.

### 2.3 Mom Test 증거

| # | 인용 | 연결 |
|---|------|------|
| E1 | “20분 걸렸는데 못 풀었어. **대각선 하나를 빼먹었**거든” | 10선 전부 검사 |
| E2 | “**다 채우고 나서**” (틀림 발견) | 줄 단위 즉시 식별 |
| E3 | “**두 칸만 고쳤어**” → “다시 더해서 맞췄지” | `failed_lines`로 수정 대상 좁히기 |

### 2.4 표면 문제 (범위 밖 정의)

- ECB/BCE 전체 분류표만 작성
- `Solver` / `GridUI` / 프로그램부터 제작
- 테스트 없는 실패 조건 도출만

---

## 3. R-G-I-O

| | 내용 |
|---|---|
| **R — Role** | 부분 마방진 학습자. 빈칸 2개를 채운 뒤 맞았는지 **스스로 확인** |
| **G — Goal** | 10선 합 34 **즉시 판정**, 틀리면 **행·열·대각선 ID** 식별 |
| **I — Input** | `grid: list[list[int]]` — 4×4. 셀: `0`(빈칸) 또는 `1~16` |
| **O — Output** | `validate_lines(grid)` → `{ status, failed_lines }` (§5) |

---

## 4. 도메인 · Rule

### 4.1 Entity

| 항목 | 규격 |
|------|------|
| 격자 | `grid: list[list[int]]`, 4×4 |
| 셀 | `0` = 빈칸, `1`~`16` = 채운 값 |
| MAGIC | `34` (`entity.constants.MAGIC`) |
| GRID_SIZE | `4` |
| CELL_MAX | `16` |

### 4.2 10선

| ID | 설명 |
|----|------|
| `row:0` ~ `row:3` | 행 R1~R4 |
| `col:0` ~ `col:3` | 열 C1~C4 |
| `diag:main` | 주대각 D1 |
| `diag:anti` | 부대각 D2 |

### 4.3 Rule (판정)

| Rule | 내용 |
|------|------|
| R1~R4 | 각 **행** 합 = MAGIC |
| C1~C4 | 각 **열** 합 = MAGIC |
| D1, D2 | 각 **대각선** 합 = MAGIC |
| **R5** | 격자에 `0`이 **하나라도** 있으면 → `status=incomplete`, **합 검증 생략**, `failed_lines=[]` |

10선 **전부** 검사. 대각선 누락 금지.

### 4.4 예시 격자 G1 (과제 슬라이드)

빈칸 2개 — row-major `(1,3)`, `(2,2)` (0-index):

| 16 | 3 | 2 | 13 |
| 5 | 10 | 11 | **0** |
| 9 | 6 | **0** | 12 |
| 4 | 15 | 14 | 1 |

완성 격자 `VALID_GRID` (테스트 fixture):

| 16 | 3 | 2 | 13 |
| 5 | 10 | 11 | 8 |
| 9 | 6 | 7 | 12 |
| 4 | 15 | 14 | 1 |

---

## 5. Command API

### 5.1 `validate_lines`

- **위치:** `src/validate_lines.py`
- **역할:** 10선 합 계산 + MAGIC 비교의 **유일한 진입점**

```python
def validate_lines(grid: list[list[int]]) -> dict:
    ...
```

### 5.2 반환 계약

```python
{
    "status": "pass" | "fail" | "incomplete",
    "failed_lines": [
        {"id": str, "sum": int, "expected": int},  # expected == MAGIC
        ...
    ],
}
```

| status | 조건 | failed_lines |
|--------|------|--------------|
| `pass` | `0` 없음, 10선 모두 합 MAGIC | `[]` |
| `fail` | `0` 없음, 하나 이상 합 ≠ MAGIC | **틀린 줄만** |
| `incomplete` | `0` 하나라도 (R5) | `[]` |

### 5.3 ECB (세션 3 범위)

| 계층 | 세션 3 | 비고 |
|------|--------|------|
| Entity | 도메인·상수 | `entity/constants.py` (GREEN 이후 SSOT) |
| Command | `validate_lines` | Control 계층 |
| Boundary | **없음** | `ResultDisplay` — 다음 세션 |
| Test Loop | RED → GREEN → REFACTOR | ARRR 연동 |

- entity → boundary/control **import 금지**
- E001~E005 오류코드 **emit 금지** (세션 3)

---

## 6. Functional Requirements (FR)

| ID | 요구사항 | Mom Test |
|----|----------|----------|
| **FR-1** | `validate_lines(grid)` 한 번으로 **10선×MAGIC** 검증 (행4+열4+대각2) | E1 |
| **FR-2** | 완성 격자 → `status=pass`, `failed_lines=[]` | E1 |
| **FR-3** | `0` 포함 격자 → `status=incomplete`, `failed_lines=[]`, 합 검증 생략 (R5) | — |
| **FR-4** | 합≠MAGIC 이고 `0` 없음 → `status=fail`, 틀린 줄만 `failed_lines` | E2, E3 |
| **FR-5** | `failed_lines` 항목에 `id`, `sum`, `expected`(MAGIC) 포함 | E2, E3 |
| **FR-6** | Test Loop RED→GREEN→REFACTOR, assert·구현·리팩터 단계 분리 | E1 (20분 재현 방지) |

### 6.1 범위 밖 (Non-FR)

| 항목 | 사유 |
|------|------|
| 1~16 중복·범위 검증 | 합 34 판정 집중 |
| `Solver` / 빈칸 자동 채우기 | 고통은 검증·확인 비용 |
| `GridUI` / `InputHandler` | 표면 솔루션 |
| ECB 전체 앱 / 분류표만 | 재현·테스트 없는 설계 |
| `MagicSquare` / `Cell` Entity 클래스 | 다음 세션 |

---

## 7. Test Requirements · Test ID

### 7.1 RED 묶음 1 (구현됨 — assert RED)

| Test ID | FR | 함수명 | Given | Then |
|---------|-----|--------|-------|------|
| **T1** | FR-2 | `test_pass_when_all_ten_lines_sum_to_magic` | `VALID_GRID` | `pass`, `[]` |
| **T2** | FR-4 | `test_fail_reports_wrong_line_id_and_sum` | `grid[0][0]=99` | `fail`, `row:0` + sum |
| **T3** | FR-3 | `test_incomplete_when_grid_contains_zero` | `grid[0][0]=0` | `incomplete`, `[]` |

### 7.2 RED 후보 (미구현)

| Test ID | 시나리오 |
|---------|----------|
| T4 | `diag:main` 실패 보고 |
| T5 | 복수 `failed_lines` |
| T6 | `diag:anti` 실패 |
| D-LOC-01 | `grid_g1` 빈칸 좌표 row-major |

### 7.3 C2C Rule 1~3 (설계 시)

| Rule | 내용 |
|------|------|
| Rule1 | FR 원문 인용 |
| Rule2 | FR → To-Do 1개 |
| Rule3 | Test ID + Given / When / Then |

---

## 8. TDD · ARRR · Dual-Track

### 8.1 ARRR ↔ TDD

| ARRR | TDD | Command |
|------|-----|---------|
| **Ask** | RED ③④ | `/red-test-plan`, `/red-skeleton` |
| **Ask** | RED assert | `/tdd-red` |
| **Respond** | GREEN | `/green-minimal` |
| **Respond** | Golden | `/golden-master` |
| **Refine** | smell ⑦ | `/refactor-smell` |
| **Refine** | safe | `/refactor-safe` |

**Command 체인:**

```
/red-test-plan → /red-skeleton → /tdd-red
  → /green-minimal → /golden-master
  → /refactor-smell → /refactor-safe
```

### 8.2 Phase 선언 (응답 첫 줄)

| 단계 | 형식 |
|------|------|
| RED | `Phase: red \| Layer: entity \| Track: Logic` |
| GREEN | `Phase: green \| Layer: entity \| Track: Logic` |
| REFACTOR smell | `Phase: refactor \| Scope: src/ tests/ \| Track: Logic+UI` |
| REFACTOR safe | `Phase: refactor \| Layer: entity \| Track: Logic` |

### 8.3 Dual-Track

| | Track B — Logic | Track A — UI (Boundary) |
|---|-----------------|-------------------------|
| Layer | `entity` | `boundary` |
| 테스트 | dict 직접 assert | 표시·포맷 (다음 세션) |
| Mock | Domain Mock **금지** | Boundary Mock (UI 세션) |

세션 3 기본: **Track B · Logic**.

### 8.4 GREEN 규칙

- **1커밋 = 1 RED 묶음**
- 상수 SSOT: `entity.constants` — 리터럴 `34`/`16`/`4` 금지
- REFACTOR·기능 추가·버그 수정은 별도 단계

### 8.5 REFACTOR 규칙

- Change Budget: 파일 ≤3 · 클래스 ≤1 · 메서드 ≤3
- 스멜 1개씩 `/refactor-safe`
- 입출력·`int6` 1-index·golden `codes` 포맷 **불변**

---

## 9. Golden Master (Approval Test)

| 항목 | 규격 |
|------|------|
| 헬퍼 | `tests/_approval.py` — `assert_matches_golden` |
| 파일 | `tests/golden/{id}.approved.txt` |
| 갱신 | `UPDATE_GOLDEN=1` pytest **만** — 수동 편집 금지 |
| 포맷 | 3행: `status=` / `int6=` (6개, **1-index**) / `codes=` |
| codes | `INC:zero`, `LINE:{id}` — E001~E005 금지 |

---

## 10. 프로젝트 구조

### 10.1 현재 (RED 완료)

```
MagicSquare_XX/
├── .cursorrules
├── .cursor/
│   ├── commands/          # tdd-red, red-test-plan, red-skeleton, …
│   └── skills/
│       ├── magic-square-tdd/
│       └── magic-square-docs/
├── docs/
│   └── PRD.md             # 본 문서
├── pyproject.toml
├── src/
│   ├── __init__.py
│   └── validate_lines.py  # 시그니처 + MAGIC (본문 미구현)
├── tests/
│   ├── __init__.py
│   └── test_validate_lines.py  # T1~T3 RED
├── Report/                # 세션 보고서 NN.*
└── Prompting/             # Transcript NN.*
```

### 10.2 GREEN 이후 (계획)

```
src/entity/constants.py    # MAGIC, GRID_SIZE, CELL_MAX
tests/conftest.py          # grid_g1 fixture
tests/_approval.py         # golden helpers
tests/golden/*.approved.txt
```

---

## 11. 구현 상태

| 항목 | 상태 |
|------|------|
| Harness · `.cursorrules` | ✅ |
| ARRR Commands · Skills | ✅ |
| T1~T3 RED 테스트 | ✅ (`3 failed` — 의도적) |
| `validate_lines` 구현 | ❌ GREEN 대기 |
| `entity/constants.py` | ❌ GREEN 시 추가 |
| Golden · conftest `grid_g1` | ❌ 선택 (post-GREEN) |
| REFACTOR | ❌ PASS 후 |

**최근 pytest (RED):** `3 failed` — `TypeError: 'NoneType' object is not subscriptable` (`validate_lines` → `None`).

---

## 12. 성공 기준 (Acceptance)

| # | 기준 | 증거 | 현재 |
|---|------|------|------|
| AC-1 | FR-1: 10선×34 Command | T1 설계 | RED ✅ / GREEN ❌ |
| AC-2 | FR-2~4: pass / fail / incomplete | T1~T3 | RED ✅ |
| AC-3 | FR-5: `failed_lines` id·sum·expected | T2 assert | RED ✅ |
| AC-4 | `python -m pytest tests/ -v` 전부 PASS | — | ❌ |
| AC-5 | (선택) golden matched | — | ❌ |

---

## 13. 비기능 요구사항

| ID | 요구 |
|----|------|
| NFR-1 | Python ≥ 3.10, pytest (`pyproject.toml`) |
| NFR-2 | `pythonpath = ["src"]` |
| NFR-3 | AI·Command 응답 한국어 |
| NFR-4 | `git commit` — 사용자 명시 요청 시만 |
| NFR-5 | Export: `/export-session` + `magic-square-docs` Skill |

---

## 14. 관련 문서

| 문서 | 경로 |
|------|------|
| Cursor Rules | `.cursorrules` |
| Mom Test · 워크북 | `Report/03.REPORT.md` |
| Harness · RED | `Report/04.Harness-TDD-RED_REPORT.md` |
| Export 워크플로 | `Report/05.Export-Session_REPORT.md` |
| TDD Skill | `.cursor/skills/magic-square-tdd/SKILL.md` |
| Docs Skill | `.cursor/skills/magic-square-docs/SKILL.md` |

---

## 15. 로드맵

| 순서 | 작업 | Command |
|------|------|---------|
| 1 | GREEN — `validate_lines` 최소 구현 | `/green-minimal` |
| 2 | Golden baseline (선택) | `/golden-master` |
| 3 | Safe refactor | `/refactor-smell` → `/refactor-safe` |
| 4 | 추가 RED (T4~T6, 대각선·복수 실패) | `/red-test-plan` → … |
| 5 | Boundary · Solver · UI | 세션 4+ |

---

*본 문서는 `docs/PRD.md` — MagicSquare_XX Product Requirements Document v1.0 (2026-06-10).*
