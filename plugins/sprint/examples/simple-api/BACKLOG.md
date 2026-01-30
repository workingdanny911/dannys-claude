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

### F1: User Authentication
> User authentication API (login, signup, token refresh)

**Design**: [refs/designs/F1-user-auth.md](refs/designs/F1-user-auth.md)
**Context**: [active/F1-user-auth.md](active/F1-user-auth.md)

- [x] T1.1: Login API `done`
  - [x] T1.1.1: Define request/response schema
  - [x] T1.1.2: Implement endpoint
  - [x] T1.1.3: Add validation
- [x] T1.2: Signup API `done`
- [ ] T1.3: Token Refresh API #danny `in_progress`
- [ ] T1.4: Review & Refactor F1 `backlog`

---

### F2: User Profile
> User profile management (view, update)

**Design**: [refs/designs/F2-user-profile.md](refs/designs/F2-user-profile.md)

- [ ] T2.1: Get Profile API `backlog`
- [ ] T2.2: Update Profile API `backlog`
- [ ] T2.3: Review & Refactor F2 `backlog`

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
