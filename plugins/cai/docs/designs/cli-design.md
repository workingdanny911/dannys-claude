# CAI CLI — Design Specification

```yaml
type: decision
status: accepted
date: 2026-04-06
authors: [Danny, Claude]
```

---

## 1. Problem

AI agent가 context/ 디렉토리에 49+ 문서가 있을 때, 현재 작업에 관련된 문서를 효율적으로 찾을 방법이 없다. rules file이 "관련 spec을 찾아라"라고 지시하지만, AI가 직접 glob/grep하는 것은 불안정하고 비효율적.

## 2. Solution

Python CLI 도구 (`tools/cai.py`)를 제공. AI가 Bash tool로 호출하여 context 검색, 영향 분석, 상태 관리를 수행.

## 3. Design Decisions

| # | 결정 | 이유 |
|---|------|------|
| 1 | 사용자: AI only | 개발자는 직접 호출하지 않음. 출력은 AI 파싱 최적화. |
| 2 | Python + pyyaml | frontmatter 파싱이 핵심. regex보다 pyyaml이 견고. 외부 패키지는 이것만. |
| 3 | 서브커맨드 스타일 | `./tools/cai.py <command> [args]` |
| 4 | 기본 텍스트 + `--json` | 텍스트가 기본, `--json` 플래그로 JSON 전환 |
| 5 | Positional argument 자동 감지 | 파일/디렉토리/모듈 이름을 자동 판별 |
| 6 | 검색 결과에 snippet 포함 | 경로만이 아니라 매칭된 라인 범위 + 본문 미리보기 |

## 4. Commands

### 4.1 검색/탐색

#### `suggest <target>`

파일, 디렉토리, 또는 모듈 이름을 받아 관련 context 문서 + snippet 반환.

```bash
./tools/cai.py suggest src/auth/service.ts    # 파일
./tools/cai.py suggest src/auth/              # 디렉토리
./tools/cai.py suggest auth                   # 모듈 이름
```

로직:
1. covers 필드 매칭 (context/**/*.md frontmatter 스캔)
2. convention-based 매핑 (Source roots + 디렉토리 구조)
3. tag 기반 확장 (매칭된 문서의 tags로 추가 관련 문서 탐색)
4. 결과마다 관련 snippet 추출 (heading + 본문 미리보기)

Target 판별:
1. 경로가 파일이면 → 해당 파일의 모듈 식별 후 관련 문서 탐색
2. 경로가 디렉토리면 → 해당 디렉토리를 모듈로 간주
3. 이름만 주면 → specs/{name}/_overview.md 존재 여부로 모듈 매칭

#### `search <keywords>`

키워드/개념 기반 검색. 여러 키워드는 공백 구분, OR 검색. 매칭 키워드 수가 많을수록 relevance 상승.

```bash
./tools/cai.py search "환불 refund"
```

로직:
1. 키워드 분리 (공백 기준)
2. 전체 context/**/*.md 대상:
   a. frontmatter tags 매칭
   b. 문서 제목(# heading) 매칭
   c. 본문 키워드 매칭
3. 매칭 키워드 수 × 매칭 위치 가중치(tag > 제목 > 본문)로 relevance 산출
4. 매칭된 라인 주변 context를 snippet으로 추출

#### `budget --task <description> [-n N]`

태스크 설명 기반으로 가장 관련 높은 TOP N 문서 반환 (기본 10).

```bash
./tools/cai.py budget --task "결제 환불 플로우 수정" -n 5
```

로직:
1. task description에서 키워드 추출
2. 5개 신호 점수 합산:
   - tag overlap (0-5점)
   - dependency proximity (0-5점)
   - recency (0-3점, last_synced 기준)
   - confidence (0-2점, verified=2, reviewed=1, draft/intent=0)
   - type weight (0-3점, spec/convention=3, decision=2, issue=1, roadmap=0)
3. 총점 기준 TOP N 반환
4. snippet 포함

#### `impact <target>`

변경 시 영향받는 모듈/spec을 전체 의존성 그래프에서 추적. target은 파일, 디렉토리, 모듈 이름 모두 가능.

```bash
./tools/cai.py impact src/auth/service.ts
./tools/cai.py impact auth
```

로직:
1. target 판별 (suggest와 동일)
2. specs/_overview.md의 module_dependencies 맵 로드
3. 각 모듈 _overview.md의 depends_on + exports 로드
4. 전체 의존성 그래프 구축
5. 대상 모듈에서 BFS로 downstream 모듈 전부 추적
6. 각 영향받는 모듈의 관련 spec + 의존 인터페이스 snippet 출력

출력 예시:
```
Module: auth
Exports affected: AuthService.validateToken() (src/auth/service.ts:15)

Impact graph:
  auth
  ├── payment (depends_on: auth.validateToken)
  │   └── context/specs/payment/_overview.md L22: "validates token before charge"
  │   └── billing (depends_on: payment.processCharge)
  │       └── context/specs/billing/_overview.md L8: "receives verified charges"
  └── notification (depends_on: auth.validateToken)
      └── context/specs/notification/_overview.md L14: "checks auth before send"

4 modules affected (2 direct, 2 indirect)
```

### 4.2 상태/관리

#### `status`

전체 context 건강 상태 요약.

```bash
./tools/cai.py status
```

출력: 전체 문서 수, type별 분포, stale/draft/verified 비율, 마지막 onboarding 날짜.

#### `list [--type <type>] [--tag <tag>]`

문서 목록 필터링.

```bash
./tools/cai.py list --type spec
./tools/cai.py list --tag auth
./tools/cai.py list --type decision --tag payment
```

#### `diff <target>`

spec의 last_synced 이후 관련 소스 코드의 변경 내역.

```bash
./tools/cai.py diff context/specs/auth/_overview.md
./tools/cai.py diff auth
```

로직:
1. spec의 last_synced, covers 읽기
2. covers 또는 convention-based 매핑으로 소스 파일 결정
3. `git log --since="{last_synced}" -- {소스 파일들}`
4. `git diff` 요약 — 변경된 함수/클래스 단위
5. snippet 포함

#### `validate [--fix]`

frontmatter 스키마 검증. 필수 필드 누락, enum 값 오류 등.

```bash
./tools/cai.py validate
./tools/cai.py validate --fix    # 자동 수정 가능한 것은 수정
```

#### `update-synced <target>`

특정 문서의 last_synced를 오늘로 갱신.

```bash
./tools/cai.py update-synced context/specs/auth/_overview.md
```

## 5. Output Format

### 텍스트 모드 (기본)

```
[high] context/specs/payment/refund-flow.md (spec, draft)
  L12-28: ## Refund Process
          RefundService handles all refund requests through a 3-step flow...

[med]  context/decisions/007-async-refund.md (decision, accepted)
  L5-8:   환불을 동기 처리에서 비동기 큐로 전환.

3 documents found (2 high, 1 medium)
```

### JSON 모드 (`--json`)

```json
{
  "results": [
    {
      "path": "context/specs/payment/refund-flow.md",
      "type": "spec",
      "confidence": "draft",
      "relevance": "high",
      "reason": "convention-based mapping: src/payment/** → specs/payment/",
      "snippets": [
        {"lines": "12-28", "heading": "## Refund Process", "text": "RefundService handles..."}
      ]
    }
  ],
  "total": 3
}
```

### Relevance 기준

- **high**: covers 직접 매칭 또는 키워드 2+ 매칭
- **medium**: convention-based 매핑 또는 키워드 1 매칭
- **low**: tag만 매칭

## 6. Rules File 연동

`cai.md`의 Pre-work 섹션에 CLI 사용법 추가:

```markdown
## Pre-work: Context loading
파일을 수정하기 전, CLI로 관련 context를 확인하라:
  ./tools/cai.py suggest <대상 파일 또는 모듈>
결과에서 high/medium 문서를 읽고 패턴을 따르라.

복잡한 작업이면 budget으로 우선순위를 확인:
  ./tools/cai.py budget --task "<작업 설명>"

변경 범위가 넓으면 impact로 영향 범위를 파악:
  ./tools/cai.py impact <대상>

전체 사용법: ./tools/cai.py --help
```

## 7. CLAUDE.md 연동

cai-init이 CLAUDE.md에 제안하는 블록:

```markdown
## Context Infrastructure
이 프로젝트는 CAI를 사용합니다.
- Knowledge base: context/
- Rules: .claude/rules/cai.md
- CLI: ./tools/cai.py <command> (suggest, search, budget, impact, diff, status, list, validate, update-synced)
```

## 8. Installation

cai-init이 자동으로 처리:

```
cai-init 실행 시:
  1. templates/tools/cai.py → tools/cai.py (복사)
  2. templates/tools/requirements.txt → tools/requirements.txt (복사)
  3. pip install pyyaml (자동 실행)
```

cai-upgrade 시에도 cai.py를 TOOL-MANAGED 파일로 업데이트.

## 9. Dependencies

- Python 3.8+
- pyyaml (유일한 외부 패키지, cai-init이 자동 설치)
- git (diff, impact에서 사용)

## 10. File Structure

```
tools/
├── cai.py              ← 단일 진입점 (TOOL-MANAGED)
├── drift-warning.js   ← 기존 PreToolUse hook (TOOL-MANAGED)
└── requirements.txt   ← pyyaml만 (TOOL-MANAGED)
```
