# Sprint Plugin - Workflow Guide

## Overall Workflow

```
┌────────────────────────────────────────────────────────────────────┐
│                        Sprint Workflow                              │
└────────────────────────────────────────────────────────────────────┘

 Phase 1: Setup              Phase 2: Planning           Phase 3: Execution
 ────────────────           ────────────────            ─────────────────
 /sprint:init               /sprint:add-backlog         @INSTRUCTION.md
       │                          │                           │
       ▼                          ▼                           ▼
 Create Sprint              Define Feature/Task         Work on Task
       │                          │                           │
       │                          ▼                           ▼
       │                   /sprint:plan-backlog        Complete Task
       │                          │                           │
       │                          ▼                           ▼
       │                   Break into Sub-tasks         End Session
       │                                                      │
       └──────────────────────────────────────────────────────┘
                                   │
                                   ▼
                            /sprint:review-backlog
                                   │
                                   ▼
                             Quality Review
                                   │
                                   ▼
                            Add Improvement Tasks (if needed)
```

---

## Phase 1: Sprint Initialization

### 1.1 Run `/sprint:init`

```
User: /sprint:init
```

### 1.2 Provide Information

Claude will ask:

1. **Sprint name**: kebab-case recommended
   ```
   e.g., payment-system, auth-refactor, dashboard-v2
   ```

2. **Location**: Default `sprints/<sprint-name>/`
   ```
   e.g., sprints/payment-system/
   ```

3. **Team (optional)**: Agent names
   ```
   e.g., #danny, #agent-1, #agent-2
   ```

### 1.3 Result

```
sprints/payment-system/
├── BACKLOG.md
├── HANDOFF.md
├── INSTRUCTION.md
├── .sprint-version
├── active/
│   └── README.md
└── refs/
    ├── designs/
    ├── plans/
    ├── decisions/
    │   └── _sprint.md
    ├── lessons/
    │   └── _sprint.md
    └── archive/
```

---

## Phase 2: Work Planning

### 2.1 Add Features

#### Run `/sprint:add-backlog`

```
User: /sprint:add-backlog
```

#### Brainstorming Process

```
Claude: What do you want to build?

User: User authentication feature

Claude: What type of work is this?
1. coding (recommended)
2. docs
3. ideation
4. general

User: 1

Claude: Let's define the scope.

Include:
- Login
- Signup
- Password reset

Anything to exclude?

User: Social login for later

Claude: What are the success criteria?

User: APIs work and tests pass
```

#### Proposed Structure

```markdown
### F1: User Authentication
> User auth (login, signup, password reset)
> Social login excluded

**Type**: coding

- [ ] T1.1: Login API `backlog`
- [ ] T1.2: Signup API `backlog`
- [ ] T1.3: Password Reset API `backlog`
- [ ] T1.4: Auth Integration Tests `backlog`
- [ ] T1.5: Review & Refactor F1 `backlog`

Proceed?

User: Yes

Claude: Added to BACKLOG.md.

Create a design document? (2+ tasks → recommended)

User: Yes

Claude: Created refs/designs/F1-authentication.md
```

### 2.2 Detailed Task Planning (Optional)

For complex Tasks, use `/sprint:plan-backlog`:

```
User: /sprint:plan-backlog T1.1
```

#### Brainstorming → Planning

```
Claude: Let's design T1.1: Login API.

Which authentication method?
1. JWT (recommended) - stateless, scalable
2. Session - server-based
3. OAuth only - external auth

User: 1

Claude: Let me verify my understanding.

## Overview
Login API authenticates with email/password and issues JWT tokens.
- Access Token: 15 min validity
- Refresh Token: 7 day validity

Correct so far?

User: Yes

[Enter Plan Mode]

Claude: I propose the following plan:

- [ ] T1.1.1: Define request/response schema
- [ ] T1.1.2: Implement login endpoint
- [ ] T1.1.3: Add input validation
- [ ] T1.1.4: Add rate limiting
```

---

## Phase 3: Execution

### 3.1 Start Session

```
User: @sprints/payment-system/INSTRUCTION.md #danny
```

### 3.2 Agent Behavior

```
Claude: Starting session as #danny.

[Reading BACKLOG.md, HANDOFF.md]

Current state:
- F1: User Authentication (4 tasks)
  - T1.1: Login API `backlog` ← Top priority
  - T1.2: Signup API `backlog`
  - ...

Claiming and starting T1.1: Login API.
```

### 3.3 Working

What Claude does:

1. **Update BACKLOG.md**
   ```markdown
   - [ ] T1.1: Login API #danny `in_progress`
   ```

2. **Update HANDOFF.md**
   ```markdown
   | F1 | T1.1: Login API | #danny | 2024-01-28 | JWT impl |
   ```

3. **Create active/ file** (if first Task for Feature)
   ```
   active/F1-user-auth.md
   ```

4. **Execute actual work**

5. **Record progress**

### 3.4 Task Completion

```
Claude: Completed T1.1: Login API.

Updates:
- BACKLOG.md: T1.1 → done
- HANDOFF.md: Moved to Recently Done
- active/F1-user-auth.md: Added completion notes

Ending session. Start new session for next Task.
```

**Important**: Agent does NOT auto-start next Task!

### 3.5 Next Task

Start new session:

```
User: @sprints/payment-system/INSTRUCTION.md #danny
```

---

## Phase 4: Review

### 4.1 Run Review

```
User: /sprint:review-backlog T1.1
```

### 4.2 Apply Checklist

Review with type-appropriate checklist (`coding`):

```
Claude: Review results for T1.1: Login API

### 🔴 Critical (1)
1. Password hashing not applied
   - Location: src/auth/login.ts:24
   - Impact: Security vulnerability

### 🟡 Improvement (2)
1. Error message exposure
   - Current: "User not found"
   - Suggestion: Use generic message

2. Rate limiting not applied
   - Suggestion: Prevent brute force

### 🟢 Minor (1)
- Variable naming could improve

Create improvement plan?

User: Yes

[Enter Plan Mode]

Claude: Adding following improvement Tasks:

- [ ] T1.6: Fix review issues (T1.1) `backlog`
  - [ ] T1.6.1: Add password hashing
  - [ ] T1.6.2: Generalize error messages
  - [ ] T1.6.3: Add rate limiting
```

---

## Multi-Agent Scenarios

### Concurrent Work

```
┌────────────────┐     ┌────────────────┐
│  Session 1     │     │  Session 2     │
│  #danny        │     │  #agent-1      │
│  T1.1 work     │     │  T2.1 work     │
└───────┬────────┘     └───────┬────────┘
        │                      │
        ▼                      ▼
   ┌────────────────────────────────┐
   │          Sprint Files          │
   │  BACKLOG.md (own Task only)    │
   │  HANDOFF.md (own row only)     │
   │  active/F1-*.md | active/F2-*  │
   └────────────────────────────────┘
```

### Conflict Prevention Rules

1. **Modify only your area**
   - BACKLOG.md: Only assigned Task
   - HANDOFF.md: Only your row
   - active/: Only your Feature

2. **Read latest version before modifying shared files**

3. **On conflict, retry**

### Handoff Scenario

#danny working, needs to end session → #agent-1 takes over:

```
# Session 1: #danny
@INSTRUCTION.md #danny
→ Start T1.2
→ Need to end session mid-work
→ Record state in active/F1-*.md
→ BACKLOG.md: T1.2 `blocked` (with reason)

# Session 2: #agent-1
@INSTRUCTION.md #agent-1
→ Read active/F1-*.md
→ Check T1.2 status, continue work
```

---

## Context Compaction Recovery

When context compaction occurs during a Claude Code session:

### Recovery Procedure

```
1. Re-read INSTRUCTION.md
2. Re-read BACKLOG.md
3. Re-read HANDOFF.md
4. Re-read active/F{n}-*.md (most important!)
5. Maintain same agent name
6. Continue in-progress Task
```

### Tips

- Update `active/` files frequently
- Record important decisions immediately in `refs/decisions/`
- Save progress periodically for complex logic

---

## Sprint Completion

### On Feature Completion

1. Mark Feature as `done` in BACKLOG.md
2. Clean up `active/F{n}-*.md` content
3. Move decisions → `refs/decisions/F{n}-*.md`
4. Move lessons → `refs/lessons/F{n}-*.md`
5. Delete `active/F{n}-*.md`
6. Move Feature content → `refs/archive/F{n}-*.md`

### On Sprint Completion

1. All Features `done`
2. Archive everything to `refs/archive/`
3. Write Sprint retrospective in `refs/lessons/_sprint.md`
