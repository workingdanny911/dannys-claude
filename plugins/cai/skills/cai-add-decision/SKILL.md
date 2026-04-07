---
name: cai-add-decision
description: "Use when recording an architecture decision as an ADR. Triggers: 'cai-add-decision', 'decision 기록', 'ADR 추가', 'add decision', '결정 기록', '아키텍처 결정'"
---
# CAI Add Decision

## Overview

Records an architecture decision as an ADR (Architecture Decision Record) in the CAI, with automatic numbering and structured format.

## When to Use

- AI identifies an architecture decision during a coding session (action routing: "새 decision 발견")
- User explicitly wants to document a decision
- During onboarding, draft-generator identifies decisions from git history
- After a design discussion where alternatives were compared and one was chosen

## Workflow

### 1. Determine Next Number

Scan `context/decisions/` directory for existing decision files. Extract the maximum NNN from filenames matching pattern `NNN-*.md`. The next number is `max + 1`, zero-padded to 3 digits.

```
context/decisions/ contents:
  001-chose-postgresql.md
  002-event-driven-arch.md
  → next number: 003
```

If `context/decisions/` is empty or has no numbered files, start at `001`.

> **CRITICAL**: Never hardcode the number. Always dynamically calculate from directory contents.

### 2. Collect Decision Content

```
Is the decision content already available in the current conversation context?
├── YES → Use it directly (Step 3)
└── NO  → Invoke context-interviewer to gather details (Step 2a)
```

**2a. Interview for Decision Content**

Invoke the `context-interviewer` agent to collect:
- What was decided?
- What problem does this solve?
- What alternatives were considered?
- Why was this alternative chosen over others?
- What are the consequences (positive and negative)?

### 3. Write ADR Document

Create `context/decisions/{NNN}-{slug}.md` with the following structure:

```yaml
---
type: decision
status: accepted
tags: [relevant, tags]
last_synced: {today, YYYY-MM-DD}
---
# {NNN}. {Decision Title}

## Background

{Problem context and why a decision was needed}

## Decision

{What was decided, stated clearly}

## Alternatives Considered

### {Alternative 1}
- Pros: ...
- Cons: ...

### {Alternative 2}
- Pros: ...
- Cons: ...

## Consequences

### Positive
- ...

### Negative
- ...
```

The `{slug}` is derived from the decision title: lowercase, words joined by hyphens, concise (e.g., "chose-postgresql", "event-driven-arch").

### 4. Confirm with User

Present the generated ADR to the user for review before writing to disk. Apply any requested changes.

## Agent Invocations

- Agent: `context-interviewer` — Collects decision details from the user when not already available
  - Invocation: `Task("Interview the user about an architecture decision. Gather: background, decision, alternatives considered, and consequences.", agent="agents/context-interviewer.md")`

## Output

| Artifact | Path | Format |
|----------|------|--------|
| ADR document | `context/decisions/{NNN}-{slug}.md` | Markdown with YAML frontmatter (Interface Contract 0.1, decision type) |

## Error Handling

| Error | Action |
|-------|--------|
| `context/decisions/` directory does not exist | Create it before proceeding |
| Filename collision (number already taken due to race) | Re-scan and recalculate |
| User declines the ADR after review | Discard the draft, do not write to disk |
| Insufficient context for meaningful ADR | Ask the user for more details rather than writing a shallow document |
