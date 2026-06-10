# Transcript Template — `Prompting/NN.Export-Transcript.md`

SSOT: [Prompting/05.Export-Transcript.md](../../../Prompting/05.Export-Transcript.md)

메타 필드 **User / Cursor / _Exported on / _Source uuid** 필수.

---

```markdown
# MagicSquare_XX — {주제} Transcript Export

| 항목 | 내용 |
|------|------|
| 프로젝트 | `c:\Users\usejen_id\Desktop\DEV\MagicSquare_XX` |
| 단계 | {Phase·Command} |
| Phase | {red \| green \| refactor \| repeat} |
| Export일 | {YYYY-MM-DD} |
| 보고서 | [Report/{NN}.{Topic}_REPORT.md](../Report/{NN}.{Topic}_REPORT.md) |
| 선행 Transcript | [Prompting/{이전NN}.Export-Transcript.md](./…) |

| User | {사용자 요청 한 줄 또는 @멘션 요약} |
| Cursor | {Agent / Command 실행 맥락} |
| _Exported on | {YYYY-MM-DD HH:MM TZ 또는 날짜만} |
| _Source uuid | {agent-transcript uuid — 없으면 `N/A`} |

---

## 페르소나

{4×4 부분 마방진 학습자 — 이번 세션 Phase 한 줄}

---

## 대화 요약

| # | 사용자 요청 | AI 산출 | 결과 |
|---|-------------|---------|------|
| 1 | … | … | ✅ / △ / ❌ |
| 2 | … | … | … |

---

## TDD · Command Transcript

### Phase: {red \| green \| refactor \| repeat}

| 항목 | 내용 |
|------|------|
| Command | {실행한 slash 목록} |
| Test ID | {…} |
| pytest | {터미널 실행 결과만 — 미실행 시 `미실행`} |
| 변경 파일 | {경로 목록} |

{Phase=red}

| 테스트/설계 | … |
| 기대 실패 | … |

{Phase=green}

| PASS Test ID | … |
| `src/` | … |
| golden | … |

{Phase=refactor}

| 스멜 후보 | … |
| safe 제목 | … |

---

## 종료 시 산출

### Commands · Skills (해당 시)

| 경로 | 역할 |
|------|------|
| `.cursor/commands/…` | … |
| `.cursor/skills/…` | … |

### 프로젝트 스냅샷

| 경로 | 상태 |
|------|------|
| `.cursorrules` | … |
| `src/…` | … |
| `tests/…` | … |

### API 계약 (고정)

```python
validate_lines(grid) -> {
    "status": "pass" | "fail" | "incomplete",
    "failed_lines": [{"id": str, "sum": int, "expected": int}, ...]
}
```

---

## 미완료 · 다음 세션

- {불릿}

---

*Export from Cursor — User: {User} · Cursor: {Cursor} · _Exported on: {날짜} · _Source uuid: {uuid} · `Prompting/{NN}.Export-Transcript.md`*
```

---

## 메타 필드 규칙

| 필드 | 채우기 |
|------|--------|
| **User** | `/export-session` 인자·이번 턴 사용자 query 요약 (1~2문장) |
| **Cursor** | 실행 Command·Skill 이름 (예: `export-session`, `magic-square-docs`) |
| **_Exported on** | Export 작성 시각 (대화 `Today's date` 또는 실제 일자) |
| **_Source uuid** | agent-transcripts JSONL uuid — 알 수 없으면 `N/A` (추측 금지) |

푸터에 네 필드를 **반복**해 추적성 유지.
