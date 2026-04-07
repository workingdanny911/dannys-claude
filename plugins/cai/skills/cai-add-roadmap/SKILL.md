---
name: cai-add-roadmap
description: "Use when recording a future plan or direction. Triggers: 'cai-add-roadmap', 'roadmap 추가', '계획 기록', 'add roadmap', '로드맵 추가', '미래 계획'"
---
# CAI Add Roadmap

## Overview

Creates a roadmap entry documenting a future plan, direction, or initiative. Uses the `cai:interview` skill to collect details since future plans cannot be inferred from code.

## When to Use

- AI discovers a future plan during conversation (action routing: "새 roadmap 항목 발견")
- User mentions upcoming work, migrations, or strategic direction
- During onboarding Phase 3, user describes future plans

## Workflow

### 1. Determine Status

Ask or infer the roadmap item's current status:

| Status | Meaning |
|--------|---------|
| `exploring` | Under consideration, not committed |
| `planned` | Committed but not started |
| `in-progress` | Active work underway |

> Note: `completed` status exists but is set by updating existing items, not by creating new ones.

### 2. Collect Content

```
Is there sufficient context in the current conversation?
├── YES → Use it directly (Step 3)
└── NO  → Invoke the cai:interview skill (Step 2a)
```

**2a. Interview for Roadmap Content**

Invoke the `cai:interview` skill. Pass:
- **Goal**: Collect the details needed to write a roadmap entry.
- **What is already known**: Anything mentioned earlier in the conversation.
- **Output target**: This skill's working memory — answers feed Step 3.
- **Seed questions**:
  - What is being planned?
  - Why is this needed? (motivation, business driver)
  - Target timeline? (optional)
  - Which existing modules/specs are affected?
  - Known risks or dependencies?

### 3. Auto-Link Related Specs

Scan `context/specs/` to find specs related to the roadmap item:
- Match by module names mentioned in the plan
- Match by tags
- Match by `covers` paths if the plan mentions specific file areas

Populate the `related_specs` frontmatter field with paths to matching specs.

### 4. Write Roadmap Document

Create `context/roadmap/{status}/{slug}.md`:

```yaml
---
type: roadmap
status: {exploring|planned|in-progress}
tags: [relevant, tags]
last_synced: {today, YYYY-MM-DD}
target: "{target, e.g., 2026-Q3}"
related_specs: [context/specs/auth/_overview.md]
---
# {Roadmap Item Title}

## Motivation

{Why this is needed, business context}

## Description

{What will be done, scope of the initiative}

## Affected Areas

{Modules, components, or systems that will be impacted}

## Risks & Dependencies

{Known risks, blockers, or dependencies}
```

The `{slug}` is derived from the title: lowercase, words joined by hyphens (e.g., "migrate-to-oauth2", "add-real-time-notifications").

### 5. Confirm with User

Present the generated roadmap item for review. Write to disk only after approval.

## Skill Invocations

- Skill: `cai:interview` — Collects roadmap details from the user (see Step 2a).

## Output

| Artifact | Path | Format |
|----------|------|--------|
| Roadmap document | `context/roadmap/{status}/{slug}.md` | Markdown with YAML frontmatter (Interface Contract 0.1, roadmap type) |

## Error Handling

| Error | Action |
|-------|--------|
| `context/roadmap/{status}/` directory does not exist | Create it before writing |
| No related specs found | Set `related_specs: []`, note this in the document |
| User provides only a vague idea | Set status to `exploring` and keep the description high-level |
| Duplicate roadmap item detected (similar slug exists) | Ask user: update existing or create separate item |
