# Refactor Smell — ARRR R단계 (Refine ⑦)

MagicSquare_XX **Refine ⑦ 전용** — `src/`·`tests/` 코드 **스멜 탐지만** 수행한다.
**수정·리팩터·commit 금지.** 다음 실행은 `/refactor-safe`.

선행: GREEN·Golden(해당 시) 완료 — **전 테스트 PASS**.
SSOT: `.cursorrules`, `entity/constants.py`, 현재 `src/`·`tests/` 트리.
**Skill:** `magic-square-tdd` Skill이 있으면 자동 따름.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 작성:

```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI
```

이후 본문을 이어간다. 코드 패치·diff·구현 제안 스니펫은 **쓰지 않는다** (후보만 기술).

---

## Refine ⑦ 범위

| 허용 | 금지 |
|------|------|
| `src/`·`tests/` **읽기**·정적 분석 | `src/`·`tests/` **수정** |
| 스멜 표 (P0/P1/P2) 작성 | 리팩터 실행·extract/rename 적용 |
| Change Budget 추정 | `git commit` (사용자 요청 전 포함 **전부** 금지) |
| `/refactor-safe` 후보 1~3개 제안 | 테스트·assert 변경 제안 |
| `python -m pytest tests/ -v` 실행 (전제 확인) | pytest 실패 상태에서 스멜 탐지 계속 |

**성공 기준:** 전 테스트 PASS 확인 + 스멜 표 + Change Budget 내 후보 1~3개.

---

## 전제 (필수)

```bash
python -m pytest tests/ -v
```

| 결과 | 조치 |
|------|------|
| **전부 PASS** | 스멜 탐지 진행 |
| **하나라도 FAIL/ERROR** | **즉시 중단** — FAIL 목록만 보고, 스멜 표·후보 **출력하지 않음** |

명령 뒤 텍스트(예: `/refactor-smell validate_lines`)가 있으면 **해당 파일·심볼 우선** 스캔.

---

## 스멜 유형 (탐지 대상)

| 유형 | 설명 | MagicSquare 힌트 |
|------|------|------------------|
| **Long Method** | 한 함수가 다중 책임·과도한 분기/루프 | `validate_lines` 본문 과다 |
| **Duplicated Code** | 동일·유사 블록 반복 | 행/열/대각 합 계산 복붙 |
| **Mysterious Name** | 의도 불명 변수·함수명 | `x`, `tmp`, `do_check` |
| **Magic Number** | 리터럴 `34`/`16`/`4`/`10` | `entity.constants` 미사용 |
| **ECB 위반** | 계층 import·책임 침범 | entity→boundary/control, Boundary가 도메인 합산 |
| **Feature Envy** | 타 계층 데이터를 과다 조작 | 테스트 헬퍼가 `src` 로직 재구현 |

---

## 우선순위 (P0 / P1 / P2)

| 등급 | 기준 | 예 |
|------|------|-----|
| **P0** | 테스트·계약·ECB·상수 SSOT 위협 — **먼저** `/refactor-safe` | Magic Number, ECB 위반, Long Method로 버그 유발 |
| **P1** | 가독성·중복 — 동작은 안전 | Duplicated Code, Mysterious Name |
| **P2** | 미미·스타일 — 여유 시 | 주석·import 순서, 사소한 naming |

- 후보는 **P0 우선** 정렬. P0 없으면 P1에서 고른다.

---

## Change Budget (`/refactor-safe` 1회 상한)

한 번의 safe 리팩터가 넘지 않을 **예상 변경 규모**:

| 항목 | 상한 |
|------|------|
| 파일 | **≤ 3** |
| 클래스 | **≤ 1** |
| 메서드(함수) | **≤ 3** |

- 스멜 후보 제안 시 **예상 소비**를 Budget 열에 적는다.
- Budget 초과 예상이면 후보에서 **제외**하거나 분할(후속 safe)로 표기.

---

## 작업 순서

1. `python -m pytest tests/ -v` 실행 — **전부 PASS** 확인 (아니면 중단 보고).
2. `magic-square-tdd` Skill 있으면 **자동 따름** (경로·ECB·상수 규칙).
3. `src/`·`tests/` 스캔 — 스멜 유형 6종 + P0/P1/P2 분류.
4. 각 스멜에 위치(파일:줄·심볼)·근거 1줄·Budget 예상 기록.
5. Change Budget 내 **후보 1~3개** 선정 (P0 우선).
6. 아래 보고 형식 제출 — **코드 수정 없음**.

---

## 보고 형식 (필수)

```markdown
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI

## pytest 전제

- `python -m pytest tests/ -v` → [N passed / 중단: K failed]

## 스멜 표

| P | 유형 | 위치 | 근거 (1줄) | Budget 예상 (파일/클래스/메서드) |
|---|------|------|------------|----------------------------------|
| P0 | Magic Number | `src/validate_lines.py:…` | 리터럴 `34` — `MAGIC` 미사용 | 1 / 0 / 1 |
| P1 | Duplicated Code | `src/validate_lines.py:…` | 행·열 합 루프 동일 | 1 / 0 / 2 |
| P2 | Mysterious Name | `tests/…` | `g` — 격자 의미 불명 | 1 / 0 / 1 |

## /refactor-safe 후보 (1~3)

| # | 우선순위 | 제안 제목 | 대상 | 유형 | Budget |
|---|----------|-----------|------|------|--------|
| 1 | P0 | `MAGIC` 상수로 치환 | `validate_lines` | Magic Number | 1/0/1 |
| 2 | P1 | 행·열 합 헬퍼 추출 | `validate_lines` | Duplicated Code | 1/0/2 |

## 다음 단계

**P0 후보 1개만** 골라 `/refactor-safe` 실행.

예: `/refactor-safe MAGIC 상수로 치환`

- 본 커맨드에서는 **수정·commit 하지 않음**.
```

---

## 스멜 탐지 체크리스트 (Logic + UI)

| # | 확인 |
|---|------|
| 1 | `34`/`16`/`4`/`10` 리터럴 — `entity.constants` 대비 |
| 2 | entity → boundary / control import |
| 3 | `validate_lines` (또는 Command) 함수 길이·분기 수 |
| 4 | 행/열/대각 계산 중복 |
| 5 | 줄 ID 문자열 하드코딩 일관성 (`row:0` 등) |
| 6 | 테스트 픽스처·헬퍼가 production 로직 복제 (Feature Envy) |
| 7 | UI Track 파일 있을 때: 표시 로직이 도메인 합산 수행 (ECB) |

---

## 금지 사항 (재확인)

- `src/`·`tests/` **어떤 파일도 수정하지 않음**
- **commit 하지 않음** (사용자 요청 전후 무관 — 본 커맨드는 항상 금지)
- 리팩터 패치·자동 fix·“이렇게 바꾸세요” **코드 블록** 제시 금지 (위치·제목·유형만)
- pytest 실패 시 스멜 표 **출력 금지**
- assert 완화·skip·xfail 제안 **금지**
- 한국어로 응답

---

## ARRR 흐름

| 단계 | 커맨드 | 산출 |
|------|--------|------|
| R | `/green-minimal` | PASS |
| R | `/golden-master` | approval (선택) |
| **R ⑦** | **`/refactor-smell`** (본 커맨드) | **스멜 표 + 후보** |
| R | `/refactor-safe` | Budget 내 안전 리팩터 |

---

## 컨텍스트

- **탐지만** — Refine ⑦은 목록화. 실제 변경은 `/refactor-safe`에서.
- 후보는 **1~3개**. 사용자는 **P0 1개**만 골라 safe 실행.
- `Scope: src/ tests/` — 설정·docs·Report는 이번 스캔 범위 밖 (요청 시만).
