# Report Template — `Report/NN.{Topic}_REPORT.md`

SSOT: [Report/05.Export-Session_REPORT.md](../../../Report/05.Export-Session_REPORT.md)

`{Topic}`·`{NN}`·`{날짜}`·Phase별 STEP 내용을 채운다.

---

```markdown
# MagicSquare_XX — {제목 한 줄}

| 항목 | 내용 |
|------|------|
| 프로젝트 | `c:\Users\usejen_id\Desktop\DEV\MagicSquare_XX` |
| 단계 | {세션 N — Phase·Command 요약} |
| Phase | {red \| green \| refactor \| repeat} |
| 보고서 생성일 | {YYYY-MM-DD} |
| 선행 문서 | [Report/{이전NN}.…](./…) |
| Transcript | [Prompting/{NN}.Export-Transcript.md](../Prompting/{NN}.Export-Transcript.md) |
| Command | {/export-session 인자 또는 주요 slash} |
| Test ID | {이번 묶음 ID 목록 또는 —} |

---

## 1. 요약

| 구분 | 결과 |
|------|------|
| {산출물 1} | {✅/❌/△ + 한 줄} |
| {산출물 2} | … |
| pytest | {실행 결과 — N passed, K failed} |
| **판정** | **{한 줄 판정}** |

{세션 맥락 1~2문장 — Mom Test·워크북 연결 (해당 시)}

---

## 2. 산출물

### 2.1 생성·수정 파일

| 경로 | 변경 |
|------|------|
| … | 신규 / +N줄 / 미변경 |

### 2.2 핵심 결정

- {불릿 2~5개}

---

## 3. TDD · Phase STEP

<!-- Phase에 맞는 하나만 상세, 나머지는 요약 또는 — -->

### STEP: RED

| 항목 | 내용 |
|------|------|
| 설계 | `/red-test-plan` — C2C·Track B·RED 묶음 |
| 스켈레톤 | `/red-skeleton` — Test ID·`pytest.fail` |
| assert RED | `/tdd-red` — 함수명·Arrange |
| pytest | {failed 수·대표 메시지} |
| `src/` | 미수정 (RED 단계) |

### STEP: GREEN

| 항목 | 내용 |
|------|------|
| RED 묶음 | {Test ID 목록} |
| PASS | {함수명} |
| `src/` | {변경 요약} |
| pytest | {N passed} |
| golden | matched / N/A |

### STEP: REFACTOR

| 항목 | 내용 |
|------|------|
| 스멜 | `/refactor-smell` — P0/P1 요약 |
| safe | `/refactor-safe` — {제목 1개} |
| Budget | {파일/클래스/메서드 실제} |
| golden | matched / ISS+UPDATE_GOLDEN / N/A |

### STEP: repeat

| ARRR | Command | 판정 |
|------|---------|------|
| Ask | red-test-plan → red-skeleton → tdd-red | … |
| Respond | green-minimal → golden-master | … |
| Refine | refactor-smell → refactor-safe | … |

---

## 4. 성공 기준 대비

| # | 기준 (03.REPORT §6.3 등) | 상태 |
|---|---------------------------|------|
| 1 | … | ✅ / △ / — |
| 2 | … | … |

---

## 5. git · 환경 스냅샷

| 항목 | 내용 |
|------|------|
| git status | {`git status --short` 요약} |
| commit | 미수행 (또는 사용자 요청 시 SHA) |

---

## 6. 다음 단계

| 순서 | 작업 | Command |
|------|------|---------|
| 1 | … | `/…` |

---

*본 문서는 `Report/{NN}.{Topic}_REPORT.md` — MagicSquare_XX {주제} 보고서입니다.*
```

---

## Phase별 §3 강조

| Phase | §3에서 채울 STEP |
|-------|------------------|
| red | **RED** 만 상세 |
| green | **GREEN** (+ golden 선택) |
| refactor | **REFACTOR** |
| repeat | **repeat** 표 + 각 STEP 1줄 요약 |
