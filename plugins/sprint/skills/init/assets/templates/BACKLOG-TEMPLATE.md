# Backlog

> Single source of truth for all work items.
> Use `/sprint:add-backlog` to add new items.

---

## Legend

**Priority**: Top-to-bottom ordering. Items at top are highest priority.

**Urgent**: Prefix with `[URGENT]` to indicate time-sensitive items.

**Assignment**: `#agent-name` indicates who is working on it.

---

## Numbering

```
F{n}      - Feature number (F1, F2, F3...)
T{f}.{t}  - Task: Feature f, Task t (T1.1, T1.2, T2.1...)
T{f}.{t}.{s} - Sub-task (T1.1.1, T1.1.2...)
```

Example: `T3.2.1` = Feature 3, Task 2, Sub-task 1

---

## Status & Transitions

```
backlog ──────► in_progress ──────► review ──────► done
                    │                  │
                    ▼                  │
                 blocked ◄─────────────┘
                    │
                    ▼
                 backlog (when unblocked)
```

| Status | Meaning |
|--------|---------|
| `backlog` | Not started, available to claim |
| `in_progress` | Being worked on (see HANDOFF.md) |
| `blocked` | Cannot proceed, waiting on dependency |
| `review` | Work complete, awaiting review |
| `done` | Reviewed and accepted |

---

## Features

*No features yet. Use `/sprint:add-backlog` to add work items.*

<!-- Example structure:

### [URGENT] F1: Feature Name
> Brief description

**Design**: [refs/designs/F1-feature-name.md](refs/designs/F1-feature-name.md)
**Context**: [active/F1-feature-name.md](active/F1-feature-name.md) (when in progress)

- [ ] T1.1: Task name `backlog`
  - [ ] T1.1.1: Sub-task
  - [ ] T1.1.2: Sub-task
- [ ] T1.2: Task name #agent-1 `in_progress`
- [x] T1.3: Task name `done`

---

### F2: Another Feature
> Description

**Design**: [refs/designs/F2-another-feature.md](refs/designs/F2-another-feature.md)

- [ ] T2.1: Task name `backlog`

-->

<!-- Worktree mode example:

### F1: Feature Name
> Brief description

**Design**: [{sprintRoot}/refs/designs/F1-feature-name.md]({sprintRoot}/refs/designs/F1-feature-name.md)
**Context**: [{sprintRoot}/active/F1-feature-name.md]({sprintRoot}/active/F1-feature-name.md)
**Branch**: feature/F1-feature-name
**Worktree**: /path/to/worktrees/F1-feature-name

- [ ] T1.1: Task name `backlog`
- [ ] T1.2: Task name `backlog`
- [ ] T1.3: Review & Refactor F1 `backlog`
- [ ] T1.4: Merge feature/F1-feature-name and clean up worktree `backlog`

-->

---

## Done

> Completed features. Keep last 3 summaries here.

*None yet.*

---

## Archiving

When a Feature is `done`:

1. Move full Feature section → `refs/archive/F{n}-name.md`
2. Leave one-line summary here:
   - `F1: Feature Name` - completed YYYY-MM-DD
