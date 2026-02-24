# Sprint Instructions

> Guidelines for agents working on this sprint.
> Start a session with: `@INSTRUCTION.md` or `@INSTRUCTION.md #your-name`

---

## Session Start

When you receive `@INSTRUCTION.md #agent-name`:

1. **Identify yourself** as `#agent-name` (or `#agent` if not specified)
2. **Read required files**:
   - `BACKLOG.md` - Find your assignment or available work
   - `HANDOFF.md` - Current work status
   - `refs/decisions/_sprint.md` - Sprint-wide constraints (if exists)
   - `refs/lessons/_sprint.md` - Sprint-wide lessons (if exists)
3. **Determine your assignment**:
   - User assigned a Feature? → Your assignment is that Feature (scope may narrow — see Step 5)
   - User assigned a Task? → Your assignment is that Task
   - Nothing specified? → Claim highest priority Task from backlog
4. **Read context**:
   - `refs/designs/F{n}-*.md` - Feature design
   - `refs/plans/F{n}-T{m}-*.md` - Task plan (if exists)
   - `refs/decisions/F{n}-*.md` - Feature-specific decisions
   - `refs/lessons/F{n}-*.md` - Feature-specific lessons (if exists)
   - `active/F{n}-*.md` - Feature working context
5. **Assess parallelism** — Does your assignment have 2+ independent sub-items?
   - Feature with independent Tasks → consider [Agent Teams](#agent-teams)
   - Task with independent Sub-tasks → consider [Agent Teams](#agent-teams)
   - **No agent teams?** → [Narrow scope to a single Task](#scope-narrowing)
6. **State your assignment and approach** before starting work

---

## Worktree Mode

> **This section applies only when `.sprint-config` has `"mode": "worktree"`.**
> In default mode, ignore this section entirely.

**Sprint Root**: `{sprintRoot}` ← absolute path, set during init

### Rules

1. **Code work** → Only in your assigned worktree
2. **Sprint files** (BACKLOG.md, HANDOFF.md, active/, refs/) → Read/write via Sprint Root absolute path
3. **Other worktrees** → **DO NOT access**. Each worktree belongs to its Feature owner.

### Working Pattern

```
┌─────────────────────────────────────────────────────┐
│  Agent Session (Worktree Mode)                       │
│                                                      │
│  1. Read sprint files ← Sprint Root                  │
│  2. Code in worktree  ← Feature's worktree path      │
│  3. Update sprint files ← Sprint Root                │
│  4. Commit code ← worktree branch                    │
└─────────────────────────────────────────────────────┘
```

### Context Compaction Recovery (Worktree Mode)

Re-read in order:
1. `{sprintRoot}/INSTRUCTION.md` — Restore guidelines + Sprint Root path
2. `{sprintRoot}/BACKLOG.md` — Find your assignment + worktree path
3. `{sprintRoot}/HANDOFF.md` — Current status
4. `{sprintRoot}/active/F{n}-*.md` — Working context + worktree path

---

## Multi-Agent Workflow

### Your Identity

Identify yourself as `#yourname` consistently in:

- BACKLOG.md task assignments
- HANDOFF.md entries
- active/ file updates

### WIP Limit

**You may only have 1 assignment in_progress at a time.**

Before claiming new work, verify:

- [ ] I have NO current assignment in_progress
- [ ] My previous work is `done`, `review`, or `blocked`
- [ ] If blocked, I documented it and am NOT claiming another

> **Violation**: If you have an assignment in_progress, you MUST complete it before claiming another.

### Claiming Tasks (Pull)

1. Read BACKLOG.md - Find unclaimed tasks (no #agent)
2. Pick highest priority:
   - `[URGENT]` items first
   - Then top-to-bottom order
3. Update BACKLOG.md: Add `#yourname`, change to `in_progress`
4. Update HANDOFF.md: Add entry to In Progress
5. Create/update context files as needed
6. Begin work

### Completing Your Work

**Self-Check** - Before marking `review`:

- [ ] Work functions as described (for each Task in assignment)
- [ ] Self-verified (tested, reviewed own work)
- [ ] No obvious bugs or regressions
- [ ] Code/docs clean and readable

**Steps**:

1. Verify against Self-Check
2. Update HANDOFF.md: Move to **In Review**
3. Update BACKLOG.md: Keep `[ ]`, status to `review`, remove `#agent`
   - **Minimal only**: Just status change. NO completion notes here.
4. Update **Up Next** in HANDOFF.md: Add newly unblocked tasks with priority
5. Update `active/F{n}-*.md` with completion notes (detailed work summary goes here)
6. If agent teams were used: **shut down teammates** (see [Agent Teams Lifecycle](#lifecycle))
7. **Report to user**: Summarize what was done and request review
8. **END SESSION** - Do NOT automatically claim next work

> **One session = One assignment.** Complete your assignment, mark `review`, and end the session.
> Tasks become `done` only after user review.

---

### Handling Review Tasks

When you encounter `review` status tasks — either directly assigned or as part of a Feature:

**Trigger conditions:**
- User instructs you to work on a `review` task
- User instructs you to work on a Feature that contains `review` tasks

**Steps:**

1. Read `active/F{n}-*.md`, related plan/design files to understand what was done
2. **Explain in detail** to the user what was accomplished in the task
3. **Request user review** — wait for their decision

**Based on user response:**

| User Decision | Action |
|---------------|--------|
| **Approve** | Mark `[x]` `done`, move to Recently Done in HANDOFF.md |
| **Request changes** | Create improvement sub-tasks or fix directly, then re-mark `review` |

---

## Feature Context Management

### When starting first task of a Feature:

1. Create `active/F{n}-name.md` from template
2. Link to design doc and any task plans
3. Document initial understanding

### While working:

1. Update active context with decisions, progress, notes
2. Keep decisions in `active/F{n}-*.md` during work

### When Feature is done:

1. Move decisions to `refs/decisions/F{n}-*.md`
2. Move lessons to `refs/lessons/F{n}-*.md`
3. Only sprint-wide insights go to `refs/decisions/_sprint.md` or `refs/lessons/_sprint.md`
4. Delete `active/F{n}-*.md`

---

## Where to Record Information

### HANDOFF.md (Sprint-Wide Status Board)

Keep it concise - tables and short notes only:

| Section | What to Update |
|---------|----------------|
| **Up Next** | Priority-ordered claimable tasks (top 3-5) |
| **In Progress** | Your task row only |
| **In Review** | Move task when ready for review |
| **Recently Done** | Move completed (keep last 5) |
| **Dependencies** | Sprint-wide task/feature dependencies |
| **Blockers** | Sprint-wide blockers only |

**Do NOT add to HANDOFF.md:**
- Feature-specific decisions or rationale
- Detailed coordination notes
- Long explanations or context

### active/F{n}-*.md (Feature Working Context)

Record all detailed information here:

| Information | Example |
|-------------|---------|
| Progress details | "Implemented login, testing refresh token" |
| Decisions | "Chose JWT over sessions because..." |
| Coordination | "Need to sync with F2 on order ID format" |
| Handoff notes | "Next: implement rate limiting, see notes below" |
| Open questions | "Redis vs DB for refresh tokens?" |
| Files modified | "src/auth/*.ts - added validation" |

> **Rule**: Feature-specific → `active/`. Sprint-wide → `HANDOFF.md` tables.

---

## Session End

Before ending your session:

1. **Update BACKLOG.md** - Task status accurate
2. **Update HANDOFF.md** - Progress documented
3. **Update active/ context** - Notes for next session
4. **If Feature done**: Move decisions to `refs/decisions/F{n}-*.md`, lessons to `refs/lessons/F{n}-*.md`

---

## Session Handoff

When another agent will continue your work:

1. Complete **Session End** checklist above
2. In `active/F{n}-*.md`, clearly document:
   - What's done
   - What's in progress (current state)
   - What's next
   - Any blockers or open questions
3. If task incomplete, mark as `blocked` with reason in BACKLOG.md
4. Next agent should read `active/` first before resuming

---

## Avoiding Conflicts (Multi-Agent)

When multiple agents work in parallel:

1. **Only modify your area**

   - BACKLOG.md: Only your assigned task's status
   - HANDOFF.md: Only your row in tables
   - active/: Only your Feature's file

2. **Before modifying shared files**

   - Read the latest version first
   - Make minimal, targeted edits

3. **If conflict detected**
   - Re-read the file
   - Re-apply only your changes
   - Do NOT overwrite others' work

---

## Agent Teams

When your assignment has **2+ independent sub-items**, consider forming a team for speed or quality.

This applies at any scope:
- **Feature assignment** — independent Tasks run in parallel
- **Task assignment** — independent Sub-tasks run in parallel

### When to Use

For speed:
- 2+ sub-items are independent of each other
- Roles are clearly separable (e.g., frontend/backend, research/implementation)
- Parallel execution would meaningfully reduce total time

For quality:
- Implementation and testing benefit from independent perspectives
- Cross-verification would catch issues a single agent might miss
- Multiple approaches worth exploring in parallel before choosing

**Do NOT use when:**
- All sub-items have sequential dependencies
- Work is simple enough that coordination overhead exceeds benefit
- Single-perspective work is sufficient

### Proposing a Team

**Always propose to the user and get approval before creating a team.**

Present:
1. Dependency analysis of sub-items (independent vs sequential)
2. Proposed team composition:

| Agent | Role | Sub-items |
|-------|------|-----------|
| lead (me) | {role} + coordination | {sub-items} |
| worker-1 | {role} | {sub-items} |

3. Execution plan (parallel phase → sequential phase → completion)

### Execution

After user approval:

| Step | Tool | Purpose |
|------|------|---------|
| 1 | `TeamCreate` | Create team + task list |
| 2 | `TaskCreate` | Add work items to team task list |
| 3 | `Task` (with `team_name`, `name`) | Spawn teammates |
| 4 | `TaskUpdate` (with `owner`) | Assign work to teammates |
| 5 | `SendMessage` | Communicate with teammates |

**Responsibilities:**

| | Lead | Teammate |
|-|------|----------|
| Sprint files (BACKLOG.md, HANDOFF.md, active/) | Updates | Does NOT touch |
| Implementation (code, tests) | Yes | Yes |
| Completion reporting | Reports to user | Reports to lead via `SendMessage` |

Lead works on their own sub-item while coordinating teammates.

### Lifecycle {#lifecycle}

- Teammates go **idle after every turn** — this is normal. Send a message to wake them.
- When teammate reports completion: review their work, update sprint files, assign next sub-item or shut down.
- **Shutdown**: `SendMessage` with type `shutdown_request` to each teammate before ending session.
- **Lead merges results**: Verify integration, resolve conflicts, update `active/F{n}-*.md`.

### In Plan Files

When writing a task plan that uses agent teams, document in the plan file:

| Item | Description |
|------|-------------|
| **Team composition** | Agent names, roles, and assigned sub-items |
| **Dependencies** | Which sub-items block others (use `blockedBy` / `blocks`) |
| **Merge point** | When and how results are integrated |

---

## Scope Narrowing

When assigned a Feature but **not using agent teams** (sequential dependencies, simple work, or user declines), narrow your working scope to a single Task.

**Rule**: One solo agent = one Task per session, even within a Feature assignment.

**Steps**:

1. Acknowledge the Feature assignment and overall context
2. Select the highest-priority incomplete Task within the Feature
3. Work on that single Task only
4. Mark it `review` and end session — next Task starts in a new session

**Why**: A Feature is multi-Task scope designed for agent teams or multi-session work. A single agent in one session is most effective focused on one Task.

> This does not apply when agent teams are used — teams can work the full Feature scope in parallel.

---

## Context Compaction Recovery

When context compaction occurs (you notice memory loss or conversation reset):

1. **Re-read essential files** in order:

   **Default mode** (relative paths):
   - `INSTRUCTION.md` - Restore your guidelines
   - `BACKLOG.md` - Find your assigned work
   - `HANDOFF.md` - Current work status
   - `active/F{n}-*.md` - Your working context (most important)

   **Worktree mode** (Sprint Root absolute paths — see [Worktree Mode](#worktree-mode)):
   - `{sprintRoot}/INSTRUCTION.md` - Restore guidelines + Sprint Root path
   - `{sprintRoot}/BACKLOG.md` - Find your assignment + worktree path
   - `{sprintRoot}/HANDOFF.md` - Current status
   - `{sprintRoot}/active/F{n}-*.md` - Working context + worktree path

2. **Restore your state**:

   - Identify yourself as the same `#agent-name`
   - Continue the assignment you were working on
   - Do NOT claim a new assignment
   - If using agent teams: read team config (`~/.claude/teams/{team-name}/config.json`), check `TaskList` for teammate status

3. **Verify before continuing**:
   - [ ] I know which assignment I was working on
   - [ ] I read the active context file
   - [ ] I understand where I left off

> **Tip**: Keep `active/F{n}-*.md` updated frequently so recovery is smooth.

---

## Plan Mode Rule

**Enter Plan Mode before starting any Phase, UNLESS:**

- A plan already exists for this work
- User explicitly says "no plan needed" or similar
- The Phase is trivial (single obvious action)

**When required:**

1. Enter Plan Mode using `EnterPlanMode` tool
2. Write a plan for the Phase
3. Wait for user approval
4. Execute the approved plan

**Plan File Requirements (IMPORTANT):**

Since context is cleared after plan approval, plan files must be **self-contained**:

- Specify sprint path as **absolute path** (e.g., `sprints/payment-system/`)
- Include Feature/Task identifier (e.g., `F1/T2`)
- List all files to reference (absolute paths)
- Read and reference relevant decisions/lessons (summarize key points in plan):
  - `refs/decisions/_sprint.md` - Sprint-wide constraints
  - `refs/lessons/_sprint.md` - Sprint-wide lessons
  - `refs/decisions/F{n}-*.md` - Feature-specific decisions (if working on F{n})
  - `refs/lessons/F{n}-*.md` - Feature-specific lessons (if exists)
- Include work context summary
- Include updating sprint files(i.e. HANDOFF.md, BACKLOG.md, etc.) according to the instruction file(<sprint>/INSTRUCTION.md)

When writing plan files, always fill in the Sprint Context section of the `refs/plans/F{n}-T{m}-*.md` template. If using agent teams, include the team composition (see [Agent Teams > In Plan Files](#in-plan-files)).

---

## Core Principles

1. **Small, Fast Feedback Loops** - Complete work incrementally, verify often
2. **Document as You Go** - Keep HANDOFF.md and active/ current
3. **Respect WIP Limits** - One assignment at a time per agent
4. **Ask Before Deciding** - Unclear? Ask user before making big decisions
5. **User Approval for Teams** - Never auto-spawn agent teams; always propose and wait for approval
