---
name: cai-onboard
description: "Use when onboarding a project into CAI. Triggers: 'cai-onboard', 'onboard', '온보딩', 'onboarding', '프로젝트 분석'"
---
# CAI Onboard

## Overview

Orchestrates the full onboarding pipeline: analyzes an existing codebase (or bootstraps a new project) and generates a complete set of CAI documents.

## When to Use

- First-time setup of CAI on a project (called by cai-init)
- Re-onboarding after major restructuring (`--incremental`)
- Resuming a previously interrupted onboarding (`--resume`)

## Flags

| Flag | Effect |
|------|--------|
| `--new` | New project mode: skip Phase 1-2 (no code to analyze), start with interview |
| `--resume` | Skip already-generated artifacts (check file existence before each step) |
| `--incremental` | Only analyze modules not yet covered by specs |
| `--force-interview` | Re-run Phase 3 even if context docs already exist |

## Workflow

### Mode Detection

```
Is --new flag set?
├── YES → New Project Flow (skip to Step N1)
└── NO  → Existing Project Flow (Step E1-E4)
```

### Existing Project Flow

#### Phase 1: Automated Analysis — Spec Generation

**E1. Structure Scan**

Invoke the `structure-scanner` agent to analyze the project's directory and file structure.

- Input: project root path
- Output: module boundary list, source roots detection, `context/specs/_overview.md` draft

After completion, write detected source roots to `cai.md` Configuration section:
```
Source roots: [detected/paths/]
```

**E2. Parallel Module Analysis**

For each module identified by structure-scanner, invoke `module-analyst` agents in parallel.

- Input: module path + structure-scanner output
- Output: `context/specs/{module}/_overview.md` draft, optional `context/specs/{module}/{component}.md` drafts

If `--incremental`: skip modules that already have `context/specs/{module}/_overview.md`.
If `--resume`: skip any spec file that already exists.

**E3. Verification (MANDATORY — DO NOT SKIP)**

<HARD-GATE>
You MUST invoke the verification-agent after E2 completes. Do NOT proceed to Phase 2 without running verification. This is non-negotiable. If you skip this step, the generated specs may contain hallucinated claims that will mislead future AI sessions.
</HARD-GATE>

Invoke the `verification-agent` to cross-validate all generated spec drafts against actual source code.

- Input: all draft specs from E1-E2
- Output: verification report (✓ confirmed / ✗ incorrect / ? uncertain), corrected drafts

Display verification results to user in this format before proceeding:
```
[Verification] 30 specs 검증 완료
  ✓ Confirmed: 85 claims
  ✗ Incorrect: 3 claims (자동 수정됨)
  ? Uncertain: 5 claims (confidence 하향)
```

Do NOT proceed to E4 until verification is complete and results are displayed.

#### Phase 2: Automated Draft Generation — Non-Spec Documents

**E4. Draft Generation**

Invoke the `draft-generator` agent to produce initial context documents from code analysis.

- Input: git log, blame data, code analysis (TODO/FIXME markers, complexity metrics, repeated patterns), existing README/docs
- Output:
  - `context/decisions/*.md` drafts (from git history patterns)
  - `context/issues/*.md` drafts (from code smells, TODOs)
  - `context/project.md` draft (from README, package.json, etc.)
- All drafts use `confidence: draft`

If `--resume`: skip document types where files already exist.

#### Phase 3: Verification Interview (BLOCKING)

> **CRITICAL**: This phase requires user interaction. Do NOT skip, automate, or bypass this phase unless `--new` was used and interview was already completed. The user MUST participate.

**E5. Context Interview**

Invoke the `context-interviewer` agent in interactive mode.

- Present Phase 1-2 drafts to the user for validation:
  - "Git history suggests these architecture decisions. Are they accurate?"
  - "These issues were detected in code. Any missing context?"
- Collect knowledge that cannot be extracted from code:
  - Project vision and constraints
  - Business rules and domain knowledge
  - Future plans and direction
  - Team conventions not visible in code
- Output:
  - Validated/corrected drafts
  - `context/roadmap/*.md` documents (code cannot infer future plans)
  - Additional decisions, issues, conventions from user input

If `--force-interview`: run even if context docs already exist.

#### Phase 4: Synthesis

**E6. Parallel Synthesis**

Invoke two agents in parallel:

1. `relationship-mapper` — maps inter-module dependencies and data flows
   - Input: all spec drafts + source code
   - Output: updated `_overview.md` files with `depends_on`, `module_dependencies` fields

2. `convention-extractor` — identifies repeated patterns across the codebase
   - Input: source code + existing specs
   - Output: `context/conventions/*.md` files (naming, error handling, testing patterns, etc.)

**E7. Constitution Assembly**

Invoke the `constitution-assembler` agent.

- Input: all generated context documents
- Output: proposed CLAUDE.md update block containing:
  - Project summary
  - Key conventions (with links to context/)
  - Architecture overview (with links to specs/)
  - Critical issues summary
  - Context infrastructure note

Present the proposed CLAUDE.md content to the user for approval. Do NOT modify CLAUDE.md without explicit user consent.

### New Project Flow

**N1. Context Interview (BLOCKING)**

Invoke the `context-interviewer` agent immediately.

- Interview topics:
  - "What are you building?" → `context/project.md`
  - "What's the tech stack?" → `context/project.md` + `context/conventions/` drafts
  - "Key architecture decisions?" → `context/decisions/*.md`
  - "Known risks or constraints?" → `context/issues/*.md`
  - "Future plans?" → `context/roadmap/*.md`

**N2. Initial Constitution Assembly**

Invoke the `constitution-assembler` agent with interview results.

- Output: proposed CLAUDE.md content
- Present to user for approval

**N3. Inform user**: "Once the project has code, run `/cai-onboard --incremental` to generate specs."

### Progress Reporting

Display phase transitions clearly:
```
[Phase 1/4] Analyzing project structure...
  ✓ Structure scan complete (5 modules found)
  ✓ Module analysis complete (5/5, 30 specs generated)
  ⏳ Verification running... (DO NOT SKIP)
  ✓ Verification: 85 confirmed, 3 corrected, 5 uncertain
[Phase 2/4] Generating document drafts...
  ✓ 3 decisions, 2 issues, 1 project doc drafted
[Phase 3/4] Interview (your input needed)...
  ...
[Phase 4/4] Synthesizing relationships and conventions...
  ✓ Dependencies mapped
  ✓ 4 conventions extracted
  ✓ CLAUDE.md update proposed
```

## Agent Invocations

- Agent: `structure-scanner` — Scans directory/file structure, identifies module boundaries
  - Invocation: `Task("Scan project structure at {project_root}. Detect source roots and module boundaries.", agent="agents/structure-scanner.md")`

- Agent: `module-analyst` — Analyzes a single module's internal structure (invoked N times in parallel)
  - Invocation: `Task("Analyze module at {module_path}. Structure scan result: {scan_result}", agent="agents/module-analyst.md")`

- Agent: `verification-agent` — Cross-validates spec claims against source code
  - Invocation: `Task("Verify these spec drafts against source code: {draft_paths}", agent="agents/verification-agent.md")`

- Agent: `draft-generator` — Generates decisions, issues, project.md from git/code analysis
  - Invocation: `Task("Generate context document drafts for project at {project_root}", agent="agents/draft-generator.md")`

- Agent: `context-interviewer` — Interactive interview for human knowledge (BLOCKING)
  - Invocation: `Task("Interview the user to validate drafts and collect missing context. Drafts: {draft_summary}", agent="agents/context-interviewer.md")`

- Agent: `relationship-mapper` — Maps inter-module dependencies
  - Invocation: `Task("Map relationships between modules. Specs: {spec_paths}", agent="agents/relationship-mapper.md")`

- Agent: `convention-extractor` — Extracts repeated patterns as conventions
  - Invocation: `Task("Extract conventions from codebase. Source roots: {source_roots}", agent="agents/convention-extractor.md")`

- Agent: `constitution-assembler` — Assembles CLAUDE.md update proposal
  - Invocation: `Task("Assemble constitution from context documents at context/", agent="agents/constitution-assembler.md")`

## Output

| Artifact | Path | Condition |
|----------|------|-----------|
| Project overview spec | `context/specs/_overview.md` | Existing project |
| Module specs | `context/specs/{module}/_overview.md` | Existing project |
| Component specs | `context/specs/{module}/{component}.md` | If modules have clear components |
| Decisions | `context/decisions/NNN-{slug}.md` | If git history reveals decisions |
| Issues | `context/issues/{slug}.md` | If code reveals issues |
| Project doc | `context/project.md` | Always |
| Roadmap items | `context/roadmap/{status}/{slug}.md` | From interview |
| Conventions | `context/conventions/{topic}.md` | Existing project |
| CLAUDE.md proposal | (displayed to user) | Always |
| Source roots config | `.claude/rules/cai.md` | Auto-detected |

## Error Handling

| Error | Action |
|-------|--------|
| structure-scanner finds no recognizable code | Suggest `--new` mode |
| module-analyst fails for one module | Continue with others, report failure, suggest re-run with `--resume` |
| verification-agent finds major inconsistencies | Display report, ask user whether to proceed or re-analyze |
| User declines interview (Phase 3) | HALT. Phase 3 is mandatory. Explain why and ask again. |
| Partial completion (interrupted) | Inform user to re-run with `--resume` |
| Source roots cannot be auto-detected | Ask user to specify source roots manually |
