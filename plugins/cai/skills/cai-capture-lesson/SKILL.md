---
name: cai-capture-lesson
description: "Use when capturing knowledge from current session. Triggers: 'cai-capture-lesson', 'lesson 기록', '교훈 캡처', '배운 것 기록', 'capture lesson', '세션 회고', '레슨 캡처'"
---
# CAI Capture Lesson

## Overview

Performs a session retrospective: reviews the current session's work, classifies learnings, and routes each item to the appropriate CAI document via the relevant cai-add-* skill.

## When to Use

- End of a productive session where debugging, design decisions, or new patterns occurred
- Action routing: "failure mode/패턴 발견" triggers this skill
- User explicitly requests a session retrospective
- AI suggests knowledge capture after resolving a non-trivial issue

> **CRITICAL**: This skill requires active session context to function. It reviews what happened in the current conversation. Do NOT invoke in a fresh session with no prior work.

## Workflow

### 1. Session Review

Review the current session's work to identify knowledge worth capturing:

- **What problems were encountered?** (bugs, errors, unexpected behaviors)
- **What solutions were found?** (root causes, fixes, workarounds)
- **What patterns were established?** (new conventions, architectural patterns)
- **What decisions were made?** (technology choices, design trade-offs)
- **What was surprising or non-obvious?** (gotchas, counterintuitive behaviors)

### 2. Classify Learnings

Categorize each identified item:

| Classification | Target Document | Routing Skill |
|---------------|----------------|---------------|
| Failure mode (bug root cause found) | Issue doc OR agent spec's Failure Modes table (Symptom-Cause-Fix) | Direct write or cai-add-spec |
| New pattern (reusable approach discovered) | Convention or spec | cai-add-spec |
| Architecture decision (alternatives compared, one chosen) | ADR | cai-add-decision |
| Future improvement idea | Roadmap item | cai-add-roadmap |

**Failure Mode format (for agent spec tables):**

| Symptom | Cause | Fix |
|---------|-------|-----|
| {Observable behavior} | {Root cause} | {Resolution steps} |

### 3. Present to User

For each classified item, present a one-line summary and proposed action:

```
Session Retrospective:

1. [Failure Mode] Redis connection timeout under load
   → Add to context/issues/redis-connection-timeout.md
   [approve / reject / edit]

2. [Pattern] Retry with exponential backoff for external API calls
   → Add to context/conventions/external-api-retry.md
   [approve / reject / edit]

3. [Decision] Chose message queue over direct HTTP for service communication
   → Create context/decisions/003-message-queue-over-http.md
   [approve / reject / edit]
```

### 4. Route Approved Items

For each item the user approves:

| Classification | Action |
|---------------|--------|
| Failure mode → new issue | Create `context/issues/{slug}.md` with severity, description, and fix |
| Failure mode → existing agent spec | Append to the Failure Modes table in the relevant agent or spec |
| New pattern → new convention | Create `context/conventions/{topic}.md` |
| New pattern → existing spec | Update the relevant spec via cai-add-spec |
| Architecture decision | Invoke cai-add-decision skill |
| Future improvement | Invoke cai-add-roadmap skill |

### 5. Summary

After all approved items are processed, display a summary:

```
Captured 3 items:
  ✓ context/issues/redis-connection-timeout.md (created)
  ✓ context/conventions/external-api-retry.md (created)
  ✓ context/decisions/003-message-queue-over-http.md (created)
```

## Agent Invocations

This skill primarily routes to other skills rather than directly invoking agents. However, for failure mode items that need to be added to agent spec tables:

- Direct file editing is used (no agent invocation needed for simple table appends)

For items routed to other skills:
- cai-add-decision is invoked for architecture decisions
- cai-add-spec is invoked for pattern documentation in specs
- cai-add-roadmap is invoked for future improvement ideas

## Output

| Artifact | Path | Format |
|----------|------|--------|
| Issue documents | `context/issues/{slug}.md` | Markdown with YAML frontmatter (issue type) |
| Convention documents | `context/conventions/{topic}.md` | Markdown with YAML frontmatter (convention type) |
| Decision documents | `context/decisions/{NNN}-{slug}.md` | Via cai-add-decision |
| Roadmap documents | `context/roadmap/{status}/{slug}.md` | Via cai-add-roadmap |
| Updated spec/agent files | Various | Appended Failure Modes rows or pattern sections |

## Error Handling

| Error | Action |
|-------|--------|
| No session context available (fresh session) | Inform user this skill requires an active session with prior work. Suggest reviewing git log instead. |
| User rejects all proposed items | Acknowledge and end gracefully. No documents created. |
| Routing to cai-add-decision fails | Fall back to direct ADR creation using the decision format |
| Target document for failure mode append does not exist | Create a new issue document instead |
