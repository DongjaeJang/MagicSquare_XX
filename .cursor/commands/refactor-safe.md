# Refactor Safe — ARRR R단계 (Safe Refactor)

MagicSquare_XX **Safe Refactor 전용** — `/refactor-smell` 표에서 **선택한 스멜 1개만** Budget 내에서 구조 정리한다.
**동작 불변** — 기능 추가·버그 수정은 **별도 GREEN**.

선행: `/refactor-smell` 완료 — 후보 표·pytest **전부 PASS**.
SSOT: 직전 스멜 표·선택 후보, `.cursorrules`, `entity/constants.py`, `tests/golden/`.
**Skill:** `magic-square-tdd` Skill이 있으면 자동 따름.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 작성:

```
Phase: refactor | Layer: entity | Track: Logic
```

- `Layer`: `entity` (기본) 또는 `boundary` (Track A — 선언만 치환)
- `Track`: `Logic` (기본) 또는 `UI`

이후 본문을 이어간다.

---

## Safe Refactor 범위

| 허용 | 금지 |
|------|------|
| **스멜 1개**에 대한 extract·rename·상수 치환·중복 제거 | 스멜 표에서 **2개 이상** 동시 해결 |
| Change Budget 내 `src/`·`tests/` 수정 | Budget 초과 (파일>3 · 클래스>1 · 메서드>3) |
| 동작 동일 전제의 구조 변경 | **기능 추가**·새 API·새 Test ID |
| | **버그 수정** (합 로직·R5·줄 ID 오류 등 — `/green-minimal`) |
| | 입출력·예외·`int6` 1-index·golden `codes` 포맷 **변경** |
| | E001~E005 `raise` / `return` / emit |
| | assert 완화·skip·xfail |
| | `git commit` (사용자 요청 전) |

**성공 기준:** `pytest tests/ -v` 전부 PASS + golden **matched** (`UPDATE_GOLDEN` 없음).

---

## 입력

`/refactor-safe` 뒤 텍스트가 **선택한 스멜 1개**를 지정한다.

```
/refactor-safe MAGIC 상수로 치환
```

- 직전 `/refactor-smell` **후보 표**에서 **1행**과 매칭되는 제목·유형·대상만 수행.
- 인자 없으면 후보 표 **#1 (P0 우선)** 을 사용. 모호하면 사용자에게 1개 확인.

---

## 불변 원칙 (Refactor 계약)

| 항목 | 불변 |
|------|------|
| **입력** | `validate_lines(grid)` 시그니처·`grid` 형식 (`4×4`, `0`/`1~16`) |
| **출력** | `{ status, failed_lines }` — status 3값·failed_lines 구조·줄 ID 규칙 |
| **예외** | 기존에 없던 raise·새 예외 타입 **추가 금지** |
| **R5** | `0` 포함 → `incomplete`, `failed_lines==[]` |
| **int6 1-index** | `canonicalize_approval`·golden `int6=` 행 — **1-index 좌표 규칙 불변** |
| **codes 포맷** | `INC:zero`, `LINE:{id}` 등 `/golden-master` 고정 토큰 **불변** |
| **E001~E005** | emit·raise·return **금지** |
| **ECB** | entity → boundary/control import **추가 금지** |
| **테스트 계약** | 기존 assert 기대값 **변경 금지** (이름만 바꿀 때 동일 의미) |

리팩터로 인해 observable 동작이 바뀌면 **롤백** — GREEN으로 분리.

---

## Change Budget (1회 상한 — `/refactor-smell`과 동일)

| 항목 | 상한 |
|------|------|
| 파일 | **≤ 3** |
| 클래스 | **≤ 1** |
| 메서드(함수) | **≤ 3** |

- 작업 시작 전 후보 표의 Budget과 대조. 초과 예상 시 **작업 분할** — 이번 safe는 중단·보고.
- 완료 후 실제 소비(파일/클래스/메서드 수)를 보고에 기록.

---

## 작업 순서

### 1. 선택 스멜 확정

- `/refactor-smell` 후보 1행: 제목 · 유형 · 위치 · Budget.
- **이번 safe는 이 1개만** — 연쇄 리팩터 금지.

### 2. Safe Refactor 적용

- 유형별 허용 작업:

| 유형 | 허용 변경 |
|------|-----------|
| Magic Number | `entity.constants` import·리터럴→`MAGIC`/`GRID_SIZE`/`CELL_MAX` |
| Duplicated Code | private 헬퍼 extract (동일 파일, 동일 반환) |
| Long Method | 조기 return·헬퍼 분리 (**로직 순서·결과 동일**) |
| Mysterious Name | 변수·함수 rename (참조 일괄, 의미 동일) |
| ECB 위반 | import 제거·책임 이동 (**계약 불변**) |
| Feature Envy | 테스트 헬퍼를 픽스처로 이동 (**assert 동일**) |

- `magic-square-tdd` Skill 있으면 **자동 따름**.

### 3. pytest — 전체 PASS

```bash
python -m pytest tests/ -v
```

- **하나라도 FAIL** → 변경 **롤백** 후 보고 (버그 수정 시 `/green-minimal` 안내).

### 4. golden matched (`UPDATE_GOLDEN` 없음)

```bash
python -m pytest tests/ -v
```

- approval 연결 테스트 포함 — env **미설정** (`UPDATE_GOLDEN` 없음).
- **matched** = golden assert PASS.

### 5. golden diff 처리

| diff 종류 | 조치 |
|-----------|------|
| **없음** | 그대로 완료 |
| **의도적** (rename만·포맷 정리로 canonical 동일 의미) | **ISS 문서화** (변경 이유 1~2줄) → `UPDATE_GOLDEN=1`로 baseline 갱신 → 다시 `UPDATE_GOLDEN` 없이 matched 확인 |
| **비의도** (status·int6·codes 값 변경) | 코드 **롤백** — golden 수동 편집 **금지** |

**ISS 문서화** — 보고 또는 `Report/`에 한 줄:

```markdown
ISS-golden: {날짜} — {스멜 제목} — canonical 불변 의도 / diff: {요약}
```

**의도적 갱신 (PowerShell):**

```powershell
$env:UPDATE_GOLDEN=1; python -m pytest tests/ -v
Remove-Item Env:UPDATE_GOLDEN -ErrorAction SilentlyContinue
python -m pytest tests/ -v
```

### 6. 보고 형식 제출

---

## 보고 형식 (필수)

```markdown
Phase: refactor | Layer: entity | Track: Logic

## 선택 스멜

| 항목 | 내용 |
|------|------|
| 제목 | MAGIC 상수로 치환 |
| 유형 | Magic Number |
| 위치 | `src/validate_lines.py` |
| Budget (예상→실제) | 1/0/1 → 1/0/1 |

## 변경 요약

- [구조 변경 2~4줄: extract/rename/상수 치환만. 동작 동일 명시]
- 변경 파일: `src/…` (+N), `tests/…` (+N) — **≤3 파일**

## pytest

- `python -m pytest tests/ -v` → **N passed** (0 failed)

## golden matched

| 항목 | 결과 |
|------|------|
| UPDATE_GOLDEN 없음 | ✅ matched / N/A (golden 미구축) |
| diff | 없음 / 의도적 — ISS: … + UPDATE_GOLDEN=1 후 matched |
| 비의도 diff | (해당 시) 롤백 완료 — safe 미완료 |

## 다음 단계

- 남은 스멜: `/refactor-smell` 재실행 또는 후보 #2 `/refactor-safe`
- commit: 사용자 요청 시 — `refactor: {스멜 제목}`
```

---

## 유형별 안전 가이드 (요약)

### Magic Number → `entity.constants`

- `src`·`tests`의 `34`/`16`/`4` → `MAGIC`/`CELL_MAX`/`GRID_SIZE`.
- **assert 기대값 숫자는 동일** (`MAGIC` import로 표현만 변경).

### Duplicated Code / Long Method

- `_sum_row`, `_line_id` 등 **private** 헬퍼. 새 public API **금지**.
- 10선 검사 **순서·누락 없음** 유지.

### Mysterious Name

- 테스트: `g` → `grid`, `r` → `result`. 함수 rename 시 pytest 이름·import 일괄.

### ECB 위반

- 잘못된 import **삭제**만. 역방향 의존 **추가하지 않음**.

---

## 금지 사항 (재확인)

- 스멜 **1개 초과** 동시 리팩터 **금지**
- Budget 초과 **금지**
- 기능 추가·버그 수정 **금지** → `/green-minimal`
- 입출력·예외·int6 1-index·codes 포맷 변경 **금지**
- E001~E005 emit **금지**
- golden **수동 편집** **금지**
- pytest 실패·비의도 golden diff 시 **롤백 없이 완료 보고 금지**
- assert 완화·skip·xfail **금지**
- 한국어로 응답

---

## ARRR 흐름

| 단계 | 커맨드 | 산출 |
|------|--------|------|
| R ⑦ | `/refactor-smell` | 스멜 표 + 후보 1~3 |
| **R** | **`/refactor-safe`** (본 커맨드) | **Budget 내 safe 1건** |
| R | `/refactor-smell` | 잔여 스멜 재스캔 (선택) |

---

## 컨텍스트

- **1 safe = 1 스멜** — 표에서 사용자가 고른(또는 #1) 후보 하나만.
- golden 없으면 §golden **N/A** — unit pytest PASS만으로 완료 가능.
- Track A: `Layer: boundary` — Boundary 표시·포맷 리팩터, 도메인 합산 로직 **이동 금지**.
