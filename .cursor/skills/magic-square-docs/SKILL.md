---
name: magic-square-docs
description: >-
  MagicSquare_XX Report and Transcript export (NN numbering, Phase STEP,
  README index). Use for Report Export, Transcript, /export-session,
  Phase repeat, ARRR 1-cycle completion reports, or session N reports.
  SSOT: Report/05, Prompting/05.
disable-model-invocation: true
---

# MagicSquare Docs — Report · Transcript Export

MagicSquare_XX 세션 기록을 `Report/`·`Prompting/`에 **NN 쌍**으로 Export.
한국어 작성. SSOT 형식: `Report/05.Export-Session_REPORT.md`, `Prompting/05.Export-Transcript.md`.

**`/export-session` 연동:** Export 요청 시 **magic-square-docs Skill 로드 후** [phase-checklist.md](phase-checklist.md) 수행.

---

## Quick Start

```
Step A → 입력 수집 (git, pytest, Phase, Test ID, Command)
Step B → NN = max(Report, Prompting) + 1
Step C → Report  ([report-template.md](report-template.md))
Step D → Transcript ([transcript-template.md](transcript-template.md))
Step E → README 문서 표 갱신 (있을 때만)
Step F → 완료 보고 (경로 2개)
```

**산출:** Report 1개 + Transcript 1개만. 기존 NN **덮어쓰기 금지**.

---

## Step A — 입력 수집

[phase-checklist.md](phase-checklist.md) 공통 C1~C7 실행.

| 입력 | 명령·출처 |
|------|-----------|
| git status | `git status --short` |
| pytest | `python -m pytest tests/ -v` |
| Phase | `red` / `green` / `refactor` / `repeat` — 채팅·Command |
| Test ID | C2C·GREEN·safe 보고 |
| Command | `/export-session`, `/green-minimal`, … |

### 금지

- **git commit** 임의 수행
- **UPDATE_GOLDEN=1** 임의 수행
- 채팅·터미널에 **없는** pytest 결과 기재 (추측·이전 세션 수치 복사 금지)
- pytest 미실행 시 → `미실행` 명시

---

## Step B — 순번 NN

1. `Report/`·`Prompting/` 파일명에서 선행 `NN` (2자리) 추출
2. `NN = max(모든 NN) + 1`
3. 동일 NN 파일 존재 시 **올리거나** 사용자 확인 — 덮어쓰기 금지

| 대상 | 패턴 |
|------|------|
| Report | `Report/NN.{Topic}_REPORT.md` |
| Transcript | `Prompting/NN.Export-Transcript.md` |

주제 `{Topic}`: `/export-session` 뒤 인자 → 없으면 대화에서 슬러그 (`ARRR-Commands`, `TDD-GREEN`).

---

## Step C — Report

템플릿: [report-template.md](report-template.md)

### Phase별 §3 STEP (하나 상세)

| Phase | STEP | 강조 내용 |
|-------|------|-----------|
| `red` | **RED** | C2C·스켈레톤·assert·pytest failed |
| `green` | **GREEN** | 묶음 PASS·`src/`·golden matched/N/A |
| `refactor` | **REFACTOR** | smell·safe 1건·Budget·golden |
| `repeat` | **repeat** | ARRR 1사이클 표 (실행한 Command만) |

필수 섹션: 요약 · 산출물 · TDD/Phase STEP · 성공 기준 대비 · git 스냅샷 · 다음 단계 · 푸터.

---

## Step D — Transcript

템플릿: [transcript-template.md](transcript-template.md)

### 필수 메타 (헤더 표 + 푸터)

| 필드 | 내용 |
|------|------|
| **User** | 사용자 요청 요약 |
| **Cursor** | Command·Skill (예: `export-session`, `magic-square-docs`) |
| **_Exported on** | Export 일시 |
| **_Source uuid** | agent-transcript uuid 또는 `N/A` |

Report와 **상호 링크** (헤더 표).

---

## Step E — README 문서 표

프로젝트 루트 `README.md`에 `## 세션 문서` (또는 동등) 섹션이 **있을 때만**:

```markdown
| NN | Report | Transcript | Phase | 주제 |
|----|--------|------------|-------|------|
| 06 | Report/06.….md | Prompting/06.Export-Transcript.md | green | … |
```

- 없으면 **건너뜀** — Step F에 `README 없음 — Step E 생략`
- README 신규 생성은 사용자 요청 없이 **하지 않음**

---

## Step F — 완료 보고 (채팅)

```markdown
## Export 완료

| 파일 | 경로 |
|------|------|
| 보고서 | Report/NN.{Topic}_REPORT.md |
| Transcript | Prompting/NN.Export-Transcript.md |

- 순번: NN
- 주제: {한 줄}
- Phase: {red|green|refactor|repeat}
- pytest: {실행 결과 또는 미실행}
```

---

## Phase: repeat (ARRR 1사이클)

`Phase: repeat` — Ask(RED) + Respond(GREEN) + Refine(REFACTOR) **완료** 후 종합 Export.

| ARRR | 포함 Command (실행분만) |
|------|-------------------------|
| Ask | `/red-test-plan` → `/red-skeleton` → `/tdd-red` |
| Respond | `/green-minimal` → `/golden-master` (선택) |
| Refine | `/refactor-smell` → `/refactor-safe` (선택) |

Report §3 **repeat** 표 + 각 STEP 1줄. 미실행 단계는 `—`.

---

## 트리거 · Command 매핑

| 트리거 | Phase | Topic 예 |
|--------|-------|----------|
| `/export-session` | 채팅에서 추출 | 인자 슬러그 |
| RED 완료 보고 | `red` | `TDD-RED` |
| GREEN 완료 보고 | `green` | `TDD-GREEN` |
| REFACTOR safe 완료 | `refactor` | `Refactor-Safe` |
| ARRR 1사이클 완료 | `repeat` | `ARRR-Cycle-1` |
| 세션 N 보고서 | 해당 Phase | `Session-N-{Phase}` |

---

## NN 이력 (참고 — Export 시 재스캔)

| NN | Report | Prompting |
|----|--------|-----------|
| 01~05 | 기존 | 기존 |
| 06+ | 이번 Step B | 이번 Step B |

항상 디스크 **재스캔** — 이 표는 참고만.

---

## Mom Test · 도메인 (해당 시)

- 4×4, 10선, 합 34, 빈칸 2개
- [Report/03.REPORT.md](../../../Report/03.REPORT.md) §6.3 성공 기준 연결
- 솔루션 최소화 — Solver·GridUI·ECB 전체 앱 범위 밖

---

## 규칙

- 한국어 · `01`~`05` 톤·표 구조 유지
- `git commit` — 사용자 요청 시만 (Export 중 **금지**)
- 파일 2개 외 생성 금지 (README 갱신은 기존 파일 **편집**만)
- magic-square-tdd Skill과 병행 시: TDD 사실은 **터미널·채팅** 우선

---

## 체크리스트 (요약)

```
[ ] Step A: git + pytest 실행·기록 (또는 미실행 명시)
[ ] Step B: NN 확인, 덮어쓰기 없음
[ ] Step C: Report — Phase STEP 맞음
[ ] Step D: User/Cursor/_Exported on/_Source uuid
[ ] Step E: README 표 (있을 때)
[ ] Step F: 경로 2개 보고
[ ] 금지: 임의 commit · UPDATE_GOLDEN · 허위 pytest
```

상세: [phase-checklist.md](phase-checklist.md)
