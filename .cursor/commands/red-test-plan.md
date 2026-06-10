# RED Test Plan — ARRR A단계 (Ask = RED ③)

MagicSquare_XX **ARRR A단계 전용** — C2C 설계표·테스트 플랜만 작성한다.
**코드·테스트 파일을 만들지 않는다.** 다음 단계는 `/red-skeleton`.

SSOT: `.cursorrules`, `docs/PRD.md`, `Report/03.REPORT.md` (PRD 없을 때 보조).

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 작성:

```
Phase: red | Layer: entity | Track: Logic
```

- `Layer`: `entity` (기본, Track B·Logic) 또는 `boundary` (Track A)
- `Track`: `Logic` (기본) 또는 `UI`
- **Track A(boundary):** 본 커맨드 본문은 그대로 두고, 선언의 `Layer`만 `boundary`로 바꾸면 재사용 가능하다. (대상 함수·Boundary 계약·Mock 규칙만 boundary에 맞게 치환)

이후 본문을 이어간다. GREEN·REFACTOR·실제 테스트 코드는 쓰지 않는다.

---

## A단계 범위

| 허용 | 금지 |
|------|------|
| C2C 설계표 (Rule1~3) 작성 | `src/` **어떤 파일도** 수정·생성 |
| Track B 표·테스트 플랜·ECB 점검 표 작성 | `tests/` **어떤 파일도** 수정·생성 |
| 채팅·PRD·`.cursorrules`에서 주제·FR·Test ID 추출 | `pytest` 실행 (다음 `/red-skeleton` 이후) |
| `conftest`·픽스처 **계획**만 기술 (파일 생성 없음) | GREEN / REFACTOR 선행 |
| | `@pytest.mark.skip`, `xfail`, assert 완화 제안 |
| | `git commit` (사용자 요청 전) |

**성공 기준:** 출력 4블록이 채워지고, `/red-skeleton`에 넘길 수 있는 수준의 테스트 플랜이 확정되어야 A단계 완료.

---

## 입력 (추가 인자 불필요)

`/red-test-plan` **만** 실행해도 동작한다. 명령 뒤 텍스트가 있으면 **해당 시나리오·FR을 우선**한다.

### 자동 추출 순서

1. **세션 주제** — `docs/PRD.md` §주제 → 없으면 `Report/03.REPORT.md` §6.1 → 없으면 채팅 맥락 한 문장
2. **Functional Requirements (FR)** — `docs/PRD.md` FR 목록 → 없으면 `.cursorrules` Rule·Command·R5 + `Report/03.REPORT.md` §6.3 성공 기준
3. **Test ID** — PRD·채팅에 이미 있으면 그대로 사용. 없으면 `T1`, `T2`, … 또는 `VAL-{시나리오}` 형태로 **이번 RED 묶음**에 맞게 부여 (한 FR·To-Do당 1 ID)
4. **대상 함수** — `.cursorrules` Command (`validate_lines` 등) 또는 PRD 명시 API
5. **Layer / Track** — 세션 3 기본값: `entity` + `Logic`. Boundary·UI 세션이면 선언만 치환

### 도메인 고정 (세션 3)

| 항목 | 값 |
|------|-----|
| 격자 | 4×4 `grid: list[list[int]]` |
| 셀 | `0`(빈칸) 또는 `1~16` |
| MAGIC | `34` |
| 10선 | `row:0`~`row:3`, `col:0`~`col:3`, `diag:main`, `diag:anti` |
| R5 | `0` 하나라도 → `status=incomplete`, `failed_lines=[]`, 합 검증 생략 |
| API | `validate_lines(grid)` → `{ status, failed_lines }` |

---

## C2C (Command-to-Contract) — Rule1~3

각 FR마다 **한 행**. Rule1~3을 한 표에 열로 둔다.

| Rule | 의미 |
|------|------|
| **Rule1** | PRD FR **원문 인용** (또는 SSOT 동등 문장) |
| **Rule2** | FR에서 도출한 **To-Do 1개** (검증 가능한 단일 행동) |
| **Rule3** | **Test ID** + **Given / When / Then** (AAA 대응) |

Given = Arrange(격자·상태), When = Act(`validate_lines` 1회), Then = Assert(반환 dict 계약).

---

## 작업 순서

1. SSOT에서 세션 주제·FR·기존 Test ID를 읽는다.
2. 이번 RED 묶음 범위를 정한다 (신규 FR만 / 기존 테스트 보강 / 명령 인자 시나리오).
3. C2C 표(Rule1~3)를 FR·To-Do·Test ID 단위로 채운다.
4. Track B 표에 Test ID별 함수·불변식·기대 RED 실패를 적는다.
5. 테스트 플랜(경로·함수명·conftest·pytest·묶음 범위)을 적는다.
6. ECB·Mock 점검 표를 채운다.
7. 아래 **보고 형식 4블록**으로 제출하고 마지막에 완료 한 줄을 쓴다.

---

## 보고 형식 (필수) — 출력 4블록

```markdown
Phase: red | Layer: entity | Track: Logic

## 1. C2C (Rule1~3)

| Test ID | Rule1 — PRD FR 인용 | Rule2 — To-Do (1개) | Rule3 — Given / When / Then |
|---------|---------------------|---------------------|-----------------------------|
| T1 | FR-…: "…" | … | **Given** … **When** … **Then** … |
| T2 | … | … | … |

- 세션 주제: [한 문장]
- RED 묶음: [이번에 설계하는 Test ID 목록]

## 2. Track B — Logic 설계표

| Test ID | 대상 함수 | Given → Then | Invariant | Expected RED Failure |
|---------|-----------|--------------|-----------|----------------------|
| T1 | `validate_lines` | 완성 격자 → `status=="pass"`, `failed_lines==[]` | 10선 전부 합 34 | `TypeError` 또는 status 불일치 (구현 없음) |
| T2 | … | … | … | … |

- Track B = Logic·entity 직접 assert (Boundary 없음)
- Track A(boundary) 전환 시: `Layer: boundary`, 대상을 Boundary 함수·표시 계약으로 치환

## 3. 테스트 플랜

| 항목 | 내용 |
|------|------|
| 테스트 파일 | `tests/test_validate_lines.py` |
| 대상 `src` | `src/validate_lines.py` — `validate_lines`, `MAGIC` |
| 테스트 함수명 (예정) | `test_pass_when_all_ten_lines_sum_to_magic`, … |
| conftest / 픽스처 (예정) | `VALID_GRID` — 표준 4×4 마방진; 변형은 `[row[:] for row in VALID_GRID]` |
| pytest 명령 | `python -m pytest tests/test_validate_lines.py -v` |
| RED 묶음 범위 | [Test ID T1~Tn — pass / fail / incomplete 등 시나리오 요약] |
| AAA | Arrange → Act(`validate_lines(grid)`) → Assert(dict 직접) |

## 4. ECB · Mock 점검

| 항목 | Logic Track (기본) | 판정 |
|------|-------------------|------|
| Domain Mock | **금지** — 실제 `grid`·`validate_lines`만 사용 | ✅ / ⚠️ |
| Boundary Mock | 세션 3 entity: 해당 없음 | — |
| E001~E005 emit | **금지** — 테스트·플랜에 오류코드 emit 없음 | ✅ |
| ECB 범위 | Rule·Command·Test Loop만. Solver·GridUI·ECB 전체 앱 제외 | ✅ |
| assert 대상 | `{ "status", "failed_lines" }` 직접 (Boundary ResultDisplay 없음) | ✅ |

---

/red-skeleton 으로 넘길 준비됐다
```

---

## 세션 3 참고 — C2C·Track B 예시 (템플릿)

이미 RED된 테스트가 있으면 **보강·추가분만** 설계한다. 전체를 다시 쓰지 않는다.

| Test ID | Rule1 (FR) | Rule2 (To-Do) | Rule3 (G/W/T) |
|---------|------------|---------------|---------------|
| T1 | FR-1: 10선×34 검증 Command | 완성 격자에서 10선 pass 판정 | G: VALID_GRID / W: `validate_lines` / T: `pass`, `[]` |
| T2 | FR-2: Red fail 재현 | 합≠34 한 줄 보고 | G: row:0 오류 / W: 호출 / T: `fail`, `failed_lines` 1건 |
| T3 | FR-3: incomplete 구분 (R5) | `0` 포함 시 합 검증 생략 | G: `grid[0][0]=0` / W: 호출 / T: `incomplete`, `[]` |

추가 RED 후보 (플랜에만, 파일 생성 없음): `diag:main` 실패, 복수 `failed_lines`, `diag:anti` 등.

---

## 금지 사항 (재확인)

- `src/`·`tests/` **파일 생성·수정 금지**
- GREEN·REFACTOR 내용·구현 스니펫 **금지**
- skip·xfail·assert 완화로 RED 우회 **금지**
- Logic Track에서 Domain·Command **Mock** 제안 **금지**
- E001~E005 등 ECB emit 오류코드를 테스트 플랜에 넣지 **않음**
- Solver, GridUI, ECB 전체, 1~16 중복 검증 등 **세션 범위 밖** 시나리오 **금지**
- 한국어로 응답

---

## 다음 단계

| 순서 | 작업 | 명령 |
|------|------|------|
| 1 | RED 스켈레톤·실패 테스트 작성 | `/red-skeleton` |
| 2 | pytest 실패 확인 | `/tdd-red` |
| 3 | 최소 구현 | `/tdd-green` (또는 사용자 요청) |

---

## 컨텍스트

- ARRR: **A**(Ask·본 커맨드) → **R**(RED·`/red-skeleton`·`/tdd-red`) → **R**(GREEN) → **R**(REFACTOR)
- `docs/PRD.md`가 없으면 `Report/03.REPORT.md` §6·`.cursorrules`를 FR SSOT로 사용하고, PRD 생성 후 FR 인용을 갱신한다.
- 명령 뒤 텍스트(예: `/red-test-plan diag:main 실패`)가 있으면 **그 시나리오를 RED 묶음에 우선** 포함한다.
