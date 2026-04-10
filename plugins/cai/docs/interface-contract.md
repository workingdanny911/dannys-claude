# CAI — Interface Contract v0.1

모든 빌드 에이전트가 작업 전에 반드시 읽어야 할 단일 규약 문서.

---

## 0.1 Frontmatter 스키마 (정확한 필드, 타입, 필수/선택)

```yaml
# === 공통 필수 (모든 context 문서) ===
type: enum[decision, issue, spec, convention, roadmap, glossary, project]  # 필수
tags: string[]      # 필수 (빈 배열 허용)
last_synced: date   # 필수, ISO 8601 (YYYY-MM-DD), tool이 자동 관리

# === spec 전용 ===
level: enum[project, module, component]  # 필수 (spec일 때)
covers: string[]     # 선택 (없으면 convention-based 매핑)
parent: string       # 자동 (상위 _overview.md 경로)
confidence: enum[intent, draft, reviewed, verified]  # 필수 (spec일 때)

# === module overview 전용 (spec + level:module 일 때 추가) ===
components: string[]   # 하위 컴포넌트 목록
exports: string[]      # public interface
depends_on: string[]   # 의존 모듈/문서 경로

# === project overview 전용 (spec + level:project 일 때 추가) ===
modules: string[]           # 전체 모듈 목록
module_dependencies: map    # { module_name: [dep1, dep2] }

# === decision 전용 ===
status: enum[proposed, accepted, deprecated, superseded]  # 필수
superseded_by: string  # 선택 (deprecated/superseded 시)

# === roadmap 전용 ===
status: enum[exploring, planned, in-progress, completed]  # 필수
target: string          # 선택 (e.g., "2026-Q3")
related_specs: string[] # 선택 (soft link)

# === issue 전용 ===
severity: enum[low, medium, high, critical]  # 필수

# === convention 전용 ===
# 공통 필드만 사용 (추가 필드 없음)

# === glossary ===
# 공통 필드만 사용 (단일 파일, type: glossary)

# === project ===
# 공통 필드만 사용 (단일 파일, type: project)
```

---

## 0.2 Skill SKILL.md 표준 포맷

```yaml
---
name: cai-skill-name       # 하이픈 구분, cai- 접두사
description: "Use when [조건]. Triggers: 'keyword1', 'keyword2'"
---
# Skill Title

## Overview
[1-2문장 요약]

## When to Use
[트리거 조건 명확히]

## Workflow
[번호 매긴 단계별 절차]

## Agent Invocations
[이 skill이 호출하는 agent 목록과 호출 방법]
- Agent: `agent-name` — 역할 설명
  - 호출: Task("지시문", agent="agent-name")

## Output
[산출물 파일 경로와 포맷]

## Error Handling
[실패 시 행동]
```

---

## 0.3 Agent .md 표준 포맷

```yaml
---
name: agent-identifier     # 하이픈 구분
description: "When to invoke this agent"
model: inherit             # 항상 inherit (사용자 모델 계승)
---
# Agent Name

## Role & Scope
[역할, 사용 가능 도구, 권한 범위]

## Inputs
[이 agent가 받는 입력 (파일 경로, 이전 agent 산출물 등)]

## Process
[단계별 작업 절차]

## Domain Knowledge
[이 에이전트 고유의 전문 지식]

## Output Format
[산출물의 정확한 형식과 저장 위치]

## Referenced Specs
[필요시 읽어야 할 문서 목록]

## Constraints
[하지 말아야 할 것]
```

---

## 0.4 Skill → Agent 호출 프로토콜

Skill의 SKILL.md는 자연어 워크플로 기술이다. Claude Code의 Agent tool (Task dispatch)을 사용하여 agent를 호출한다.

```
# 단일 호출
Agent tool로 "{agent-name}" agent를 호출하라.
프롬프트에 지시문 텍스트를 전달.

# 병렬 호출
여러 Agent tool 호출을 동시에 실행하라.

# 순차 호출
Step 1의 결과를 Step 2의 프롬프트에 포함하여 전달하라.
```

Skill은 "structure-scanner agent를 호출해서 결과를 받고, 그 결과를 module-analyst에 전달하라"고 자연어로 지시한다.

---

## 0.5 파일 네이밍 컨벤션

| 위치 | 네이밍 규칙 | 예시 |
|------|-----------|------|
| skills/ | `cai-{verb}-{noun}/SKILL.md` | `cai-add-spec/SKILL.md` |
| agents/ | `{role-name}.md` | `structure-scanner.md` |
| context/decisions/ | `NNN-{slug}.md` (3자리 번호) | `001-chose-postgresql.md` |
| context/issues/ | `{slug}.md` | `perf-n-plus-one.md` |
| context/conventions/ | `{topic}.md` | `error-handling.md` |
| context/specs/ | `{module}/_overview.md` 또는 `{module}/{component}.md` | `auth/_overview.md` |
| context/specs/ | `_relationships.md` (index) + `_relationships/{scenario}.md` | `_relationships/grading-submission-flow.md` |
| context/roadmap/ | `{status}/{slug}.md` | `planned/migrate-to-oauth2.md` |
| templates/ | 타겟 프로젝트 구조 미러링 | `templates/rules/cai.md` |

---

## 0.6 Action Routing 테이블 (Rules file 내장용)

| 상황 | Skill | 비고 |
|------|-------|------|
| spec 생성/수정 필요 | cai-add-spec | spec-writer agent 호출 → verification-agent 검증 |
| 새 decision 발견 | cai-add-decision | cai:cai-interview skill로 ADR 세부사항 수집 |
| failure mode/패턴 발견 | cai-capture-lesson | 적절한 문서(issue/agent spec/convention)에 반영 |
| 새 roadmap 항목 발견 | cai-add-roadmap | cai:cai-interview skill로 roadmap 세부사항 수집 |
| stale spec 업데이트 필요 | cai-drift-check | drift 판정 → 업데이트 제안 |
| 새 agent 필요 | cai-add-agent | agent .md 생성 + trigger table 행 추가 |

---

## 0.7 템플릿 디렉토리 구조 (cai-init이 타겟 프로젝트에 생성하는 구조)

```
templates/
├── rules/cai.md    → .claude/rules/cai.md
├── tools/drift-warning.js       → tools/drift-warning.js
├── AGENTS.md                    → AGENTS.md
└── context/                     → context/
    ├── .gitkeep
    ├── decisions/.gitkeep
    ├── issues/.gitkeep
    ├── conventions/.gitkeep
    ├── specs/.gitkeep
    ├── specs/_relationships/.gitkeep
    └── roadmap/
        ├── planned/.gitkeep
        ├── exploring/.gitkeep
        └── completed/.gitkeep

# cai-init이 복사하는 skill/agent 파일들
# skills/ → .claude/skills/ (7개: cai-onboard, cai-add-spec, cai-add-decision, cai-add-agent, cai-add-roadmap, cai-capture-lesson, cai-drift-check)
# agents/ → .claude/agents/ (11개 모두)
```

---

## 0.8 Source Roots 설정 포맷

```markdown
<!-- .claude/rules/cai.md 상단, TOOL-MANAGED 영역 -->
Context directory: context
Source roots: [src/]
```

---

## 0.9 Section Markers (cai-upgrade용)

```markdown
<!-- TOOL-MANAGED:START -->
이 영역은 cai-upgrade가 관리합니다. 수동 편집하지 마세요.
...
<!-- TOOL-MANAGED:END -->

<!-- PROJECT-SPECIFIC:START -->
이 영역은 프로젝트 고유 설정입니다. cai-upgrade가 보존합니다.
...
<!-- PROJECT-SPECIFIC:END -->
```
