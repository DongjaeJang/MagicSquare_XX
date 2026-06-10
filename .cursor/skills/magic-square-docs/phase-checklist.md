# Phase Checklist — Export 전 확인

`/export-session` 또는 ARRR 1사이클 보고 전 **Step A**에서 이 표를 채운다.
실행하지 않은 항목은 `미실행` — **추측·기재 금지**.

---

## 공통 (모든 Phase)

| # | 항목 | 수집 방법 | 기록 |
|---|------|-----------|------|
| C1 | git status | `git status --short` | 변경·untracked 목록 |
| C2 | pytest | `python -m pytest tests/ -v` | **실행 결과만** (passed/failed 수) |
| C3 | Phase 선언 | 채팅 마지막 Command | `red` / `green` / `refactor` / `repeat` |
| C4 | Test ID | C2C·GREEN 보고 | `T1`, `D-LOC-01`, … |
| C5 | Command | 이번 세션 slash | `/red-test-plan`, … |
| C6 | NN | `Report/`·`Prompting/` 스캔 | `max(NN)+1` |
| C7 | 주제 슬러그 | 명령 인자 또는 대화 | `ARRR-Commands`, `TDD-GREEN`, … |

**금지:** `UPDATE_GOLDEN=1` 임의 실행 · `git commit` 임의 · 채팅·터미널에 없는 pytest 수치

---

## RED (`Phase: red`)

| # | 확인 |
|---|------|
| R1 | `/red-test-plan` 4블록 있음 (또는 동등 설계) |
| R2 | `/red-skeleton` — `pytest.fail` 스켈레톤 (`tests/`만) |
| R3 | `/tdd-red` — assert RED, `src/` 미수정(④까지) |
| R4 | pytest **FAILED** 의도 확인 (스멜 단계 제외) |
| R5 | Test ID·함수명·변경 파일 `tests/` 목록 |

Report STEP: **RED** — 설계표·스켈레톤·assert·pytest failed 요약.

---

## GREEN (`Phase: green`)

| # | 확인 |
|---|------|
| G1 | `/green-minimal` — RED 묶음 1개 PASS |
| G2 | `entity.constants` SSOT (리터럴 34/16/4 없음) |
| G3 | 묶음 외 Test ID 상태 (FAIL 유지 여부) |
| G4 | (선택) `/golden-master` — golden 경로·matched |
| G5 | `UPDATE_GOLDEN` 없이 검증했는지 |

Report STEP: **GREEN** — PASS Test ID·`src/` 변경·pytest passed.

---

## REFACTOR (`Phase: refactor`)

| # | 확인 |
|---|------|
| F1 | `/refactor-smell` — 전 테스트 PASS 후 스멜 표 |
| F2 | `/refactor-safe` — 스멜 1개·Budget (≤3/≤1/≤3) |
| F3 | pytest 전부 PASS |
| F4 | golden matched (`UPDATE_GOLDEN` 없음) 또는 N/A |
| F5 | 비의도 golden diff 시 롤백 여부 |

Report STEP: **REFACTOR** — 선택 스멜·변경 요약·회귀 없음.

---

## repeat (`Phase: repeat`)

ARRR **1사이클** (Ask RED → Respond GREEN → Refine) 완료 보고.

| # | 확인 |
|---|------|
| P1 | RED ③④ + assert RED 기록 |
| P2 | GREEN 1묶음 PASS |
| P3 | (선택) golden baseline |
| P4 | (선택) smell + safe 1건 |
| P5 | Command 체인 표 — 실제 실행한 것만 |
| P6 | 다음 사이클 미완 항목 |

Report STEP: **repeat** — 사이클 요약 표·판정·다음 RED 묶음.

---

## Step E — README 표 (있을 때만)

`README.md`에 `## 세션 문서` 섹션이 있으면 한 행 추가:

| NN | Report | Transcript | Phase | 주제 |
|----|--------|------------|-------|------|

없으면 Step E **건너뜀** — 보고에 `README 없음` 명시.

---

## Step F — 완료 보고 (채팅)

```markdown
## Export 완료

| 파일 | 경로 |
|------|------|
| 보고서 | Report/NN.{Topic}_REPORT.md |
| Transcript | Prompting/NN.Export-Transcript.md |

- 순번: NN
- 주제: …
- Phase: …
- pytest: … (실행 결과만)
```
