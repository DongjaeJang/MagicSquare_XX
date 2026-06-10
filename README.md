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

## 테스트 (RED 묶음 1)

| ID | 시나리오 | 함수 |
|----|----------|------|
| T1 | 완성 격자 → `pass` | `test_pass_when_all_ten_lines_sum_to_magic` |
| T2 | 한 줄 오류 → `fail` + 줄 정보 | `test_fail_reports_wrong_line_id_and_sum` |
| T3 | `0` 포함 → `incomplete` | `test_incomplete_when_grid_contains_zero` |

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
├── docs/PRD.md              # 요구사항 SSOT
├── src/validate_lines.py    # Command (GREEN 대기)
├── tests/test_validate_lines.py
├── .cursor/commands/        # slash commands
├── .cursor/skills/          # TDD · Docs skills
├── Report/                  # 세션 보고서
└── Prompting/               # Transcript
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
