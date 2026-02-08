# Sprint Plugin - Core Concepts

## 1. Hierarchical Work Structure

The Sprint plugin manages work in a 3-level hierarchy.

### Feature (F{n})

- **Definition**: An independent unit of functionality that provides value to users
- **Examples**: "User Authentication System", "Payment Module", "Dashboard"
- **Characteristics**:
  - Composed of multiple Tasks
  - Design document recommended (`refs/designs/F{n}-*.md`)
  - Moved to archive when complete

```markdown
### F1: User Authentication
> User login/signup functionality

**Design**: [refs/designs/F1-user-auth.md](refs/designs/F1-user-auth.md)

- [ ] T1.1: Login API `backlog`
- [ ] T1.2: Signup API `backlog`
- [ ] T1.3: Token Refresh `backlog`
- [ ] T1.4: Review & Refactor F1 `backlog`
```

### Task (T{f}.{t})

- **Definition**: A unit of work completable in a single Claude Code session
- **Examples**: "Implement Login API", "Write tests", "Update documentation"
- **Key Constraint**: **Must be completable in one session**
- **Types**:
  - `coding` - Software development
  - `docs` - Documentation
  - `ideation` - Ideas/design
  - `general` - Other

```markdown
- [ ] T1.1: Login API `backlog`
- [ ] T1.2: Signup API #danny `in_progress`
- [x] T1.3: Token Refresh `done`
```

### Sub-task (T{f}.{t}.{s})

- **Definition**: A Task broken down into smaller steps
- **Examples**: "Define schema", "Implement endpoint", "Add validation"
- **Purpose**: Track progress on complex Tasks

```markdown
- [ ] T1.1: Login API `in_progress`
  - [x] T1.1.1: Define request/response schema
  - [ ] T1.1.2: Implement endpoint
  - [ ] T1.1.3: Add validation
```

---

## 2. Status

### Status Transition Diagram

```
backlog ──────► in_progress ──────► review ──────► done
                    │                  │
                    ▼                  │
                 blocked ◄─────────────┘
                    │
                    ▼
                 backlog (unblocked)
```

### Status Descriptions

| Status | Meaning | Notation |
|--------|---------|----------|
| `backlog` | Not started, anyone can claim | `\`backlog\`` |
| `in_progress` | In progress, agent assigned | `#agent \`in_progress\`` |
| `blocked` | Cannot proceed, waiting on dependency | `\`blocked\`` |
| `review` | Work complete, **mandatory** before done — awaiting user review | `\`review\`` |
| `done` | User reviewed and approved | `[x]` `\`done\`` |

---

## 3. Agent

### What is an Agent?

- One Claude Code session = one agent
- Identified by `#agent-name` (e.g., `#danny`, `#agent-1`)

### WIP (Work In Progress) Limit

```
┌────────────────────────────────────────┐
│  Max concurrent Tasks per agent: 1     │
└────────────────────────────────────────┘
```

**Why 1?**
- Reduce context switching costs
- Focus until completion
- Minimize conflict risk

### Agent Session Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                     Session Lifecycle                       │
└─────────────────────────────────────────────────────────────┘

  @INSTRUCTION.md #danny
         │
         ▼
  ┌─────────────┐
  │ Load Context │ ◄── Read BACKLOG, HANDOFF, active/
  └─────────────┘
         │
         ▼
  ┌─────────────┐
  │ Select Task │ ◄── Already assigned? Continue. None? Claim.
  └─────────────┘
         │
         ▼
  ┌─────────────┐
  │ Execute Task │ ◄── Do work, update active/
  └─────────────┘
         │
         ▼
  ┌─────────────┐
  │ Mark Review │ ◄── Update BACKLOG, HANDOFF (status: review)
  └─────────────┘
         │
         ▼
  ┌─────────────┐
  │ End Session │ ◄── Report to user, do NOT auto-start next Task
  └─────────────┘
```

---

## 4. Core Files

### BACKLOG.md

- **Role**: Single Source of Truth for all work items
- **Contents**: Feature list, Task list, status, priority
- **Modified When**: Task claim, status change, Feature addition

### HANDOFF.md

- **Role**: Real-time view of current progress
- **Contents**: In Progress, In Review, Blockers, Dependencies
- **Modified When**: Work start/end, blocker occurrence

### INSTRUCTION.md

- **Role**: Agent guidelines
- **Contents**: Session start/end procedures, WIP rules, conflict prevention
- **Modification**: Rarely (only on template updates)

### active/F{n}-*.md

- **Role**: Working context for in-progress Features
- **Contents**: Current state, decisions, next steps, notes
- **Lifecycle**: Created when Feature starts → Deleted when complete

### refs/ Folder

| Folder | Purpose | Lifecycle |
|--------|---------|-----------|
| `designs/` | Feature design docs | With Feature |
| `plans/` | Task execution plans | Archive after Task completion |
| `decisions/` | Decision records | Permanent |
| `lessons/` | Lessons learned | Permanent |
| `archive/` | Completed Features | Permanent |

---

## 5. Numbering System

```
F{n}        - Feature number (F1, F2, F3...)
T{f}.{t}    - Task: Feature f, Task t (T1.1, T1.2...)
T{f}.{t}.{s} - Sub-task (T1.1.1, T1.1.2...)
```

### Example

```
T3.2.1 = Feature 3, Task 2, Sub-task 1
```

### Number Assignment Rules

- Feature: Sequential increment (existing max + 1)
- Task: Sequential within Feature (T1.1, T1.2...)
- Sub-task: Sequential within Task (T1.1.1, T1.1.2...)

---

## 6. Priority

### Notation

1. **Position**: Higher = higher priority
2. **URGENT**: `[URGENT]` prefix for time-sensitive items

```markdown
### [URGENT] F1: Critical Bug Fix   ← Highest priority
> Urgent fix needed

### F2: User Dashboard              ← Second priority
> New feature

### F3: Documentation               ← Third priority
> Documentation
```

### Claiming Rules

1. `[URGENT]` items first
2. Then top-to-bottom order
3. Check dependencies (not blocked)

---

## 7. Review & Refactoring

### Review & Refactor Task

Every Feature includes a final review/refactor Task:

```markdown
- [ ] T1.1: Login API `backlog`
- [ ] T1.2: Signup API `backlog`
- [ ] T1.3: Review & Refactor F1 `backlog`  ← Required
```

### When to Add Review Tasks

| Situation | Task to Add |
|-----------|-------------|
| Feature completion | `Review & Refactor F{n}` |
| Complex Task (3+ sub-tasks) | `Review T{n}.Y` |
| Integration points | `Review integration` |

### Review Contents

- Functionality verification (confirm it works)
- Bug/edge case checks
- Code refactoring
- Remove unnecessary code/comments
- Codebase pattern consistency

---

## 8. Context Preservation

### Problem: Knowledge Loss Between Sessions

Claude Code sessions are independent → no knowledge of previous sessions

### Solution: Structured Documentation

```
┌─────────────────────────────────────────────────────────────┐
│  Session 1              Session 2              Session 3    │
│     │                      │                      │         │
│     ▼                      ▼                      ▼         │
│ ┌───────┐             ┌───────┐             ┌───────┐       │
│ │ Task A │             │ Task B │             │ Task C │      │
│ └───────┘             └───────┘             └───────┘       │
│     │                      │                      │         │
│     └──────────────────────┼──────────────────────┘         │
│                            │                                │
│                            ▼                                │
│                    ┌───────────────┐                        │
│                    │ active/F1-*.md │ ◄── Shared context    │
│                    │ refs/decisions/ │                       │
│                    │ refs/lessons/   │                       │
│                    └───────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

### What to Record

| Type | Location | Example |
|------|----------|---------|
| Progress | `active/F{n}-*.md` | "T1.2 done, T1.3 in progress" |
| Decisions | `refs/decisions/` | "JWT vs Session → chose JWT" |
| Lessons | `refs/lessons/` | "Need to unify API response format" |
| Blockers | `HANDOFF.md` | "T2.1 blocked: DB schema undefined" |
