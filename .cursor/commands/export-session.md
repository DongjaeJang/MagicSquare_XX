# Export Session — Report + Transcript

MagicSquare_XX Cursor 세션을 **Report**·**Prompting** 폴더에 `01.XXX` 순번 형식으로 Export한다.

---

## 실행 전 확인

1. `Report/`, `Prompting/` 기존 파일을 스캔해 **다음 순번 NN**을 결정한다.
2. `01`, `02`, `03` … 중 **가장 큰 NN + 1**을 사용한다. (현재 최대가 03이면 → `04`)
3. 명령 뒤 텍스트가 있으면 **주제 슬러그**로 쓴다.  
   예: `/export-session Harness TDD RED` → `Harness-TDD-RED`

주제 슬러그가 없으면 이번 대화 내용에서 **한 줄 주제**를 추출한다.

---

## 파일명 규칙 (`01.XXX` 형식)

| 대상 | 패턴 | 예시 |
|------|------|------|
| 보고서 | `Report/NN.{Topic}_REPORT.md` | `Report/04.Harness-TDD-RED_REPORT.md` |
| Transcript | `Prompting/NN.Export-Transcript.md` | `Prompting/04.Export-Transcript.md` |

- `NN`: 2자리 순번 (`01`~`99`)
- `{Topic}`: Pascal-Case 또는 kebab, 공백은 `-`로 연결
- Transcript 파일명은 **항상** `NN.Export-Transcript.md` (순번만 증가)

**같은 NN**을 Report·Prompting에 **쌍으로** 사용한다.

---

## 참조 템플릿

- Transcript 형식: `Prompting/01.Export-Transcript.md`
- 보고서 형식: `Report/01.REPORT.md`, `Report/03.REPORT.md`
- 프로젝트 규칙: `.cursorrules`

---

## Report 작성 (`Report/NN.{Topic}_REPORT.md`)

### 필수 헤더 표

```markdown
| 항목 | 내용 |
|------|------|
| 프로젝트 | `c:\Users\usejen_id\Desktop\DEV\MagicSquare_XX` |
| 단계 | [이번 세션 단계] |
| 보고서 생성일 | [오늘 날짜 YYYY-MM-DD] |
| 선행 문서 | [이전 Report 링크] |
| Transcript | [Prompting/NN.Export-Transcript.md 링크] |
```

### 필수 섹션

1. **요약** — 표: 산출물·판정·다음 단계
2. **산출물** — 생성·수정 파일, 핵심 결정
3. **TDD 상태** (해당 시) — Phase, 테스트, pytest 결과
4. **성공 기준 대비** — Mom Test·워크북 연결 (해당 시)
5. **다음 단계** — GREEN/REFACTOR 등
6. 푸터: `*본 문서는 Report/NN.{Topic}_REPORT.md — …*`

---

## Transcript 작성 (`Prompting/NN.Export-Transcript.md`)

### 필수 헤더 표

```markdown
| 항목 | 내용 |
|------|------|
| 프로젝트 | `c:\Users\usejen_id\Desktop\DEV\MagicSquare_XX` |
| 단계 | [이번 세션 단계] |
| Export일 | [오늘 날짜] |
| 보고서 | [Report/NN.{Topic}_REPORT.md 링크] |
```

### 필수 섹션

1. **페르소나** — 도메인 한 줄
2. **대화 요약** — 표: # | 사용자 요청 | AI 산출 | 결과
3. **TDD Transcript** (해당 시) — Phase, 테스트, pytest, 변경 파일
4. **종료 시 산출** — 파일 목록, API·규칙 고정 사항
5. **미완료 · 다음 세션**
6. 푸터: `*Export from Cursor … — Prompting/NN.Export-Transcript.md*`

---

## 작업 순서

1. `Report/`, `Prompting/`에서 `NN` 최댓값 확인 → 다음 번호 결정
2. 이번 대화(또는 명령 인자)에서 주제·산출·pytest 결과 수집
3. `Report/NN.{Topic}_REPORT.md` 작성
4. `Prompting/NN.Export-Transcript.md` 작성 (Report와 상호 링크)
5. 아래 보고 형식으로 사용자에게 결과 제출

**다른 파일은 만들지 않는다** — Report 1개 + Transcript 1개만.

---

## 보고 형식 (필수)

```markdown
## Export 완료

| 파일 | 경로 |
|------|------|
| 보고서 | Report/NN.{Topic}_REPORT.md |
| Transcript | Prompting/NN.Export-Transcript.md |

- 순번: NN
- 주제: [한 줄]
- TDD Phase: [RED/GREEN/REFACTOR/해당없음]
```

---

## 규칙

- 한국어로 작성
- 기존 `01`~`03` 문서 톤·표 구조 유지
- Mom Test 증거·세션 3 도메인(4×4, 10선, 34) 반영 (해당 시)
- `git commit`은 사용자 요청 시만
- 이미 같은 NN 파일이 있으면 **덮어쓰지 말고** NN을 올리거나 사용자에게 확인
