# Sprint Instructions

> Guidelines for agents working on this sprint.
> Start a session with: `@INSTRUCTION.md` or `@INSTRUCTION.md #your-name`

---

## Session Start

When you receive `@INSTRUCTION.md #agent-name`:

1. **Identify yourself** as `#agent-name` (or `#agent` if not specified)
2. **Read required files**:
   - `BACKLOG.md` - Find your task or available work
   - `HANDOFF.md` - Current work status
   - `refs/decisions/F{n}-*.md` - Feature-specific decisions (if working on F{n})
   - `refs/lessons/F{n}-*.md` - Feature-specific lessons (if exists)
   - `refs/decisions/_sprint.md` - Sprint-wide constraints (if exists)
   - `refs/lessons/_sprint.md` - Sprint-wide lessons (if exists)
3. **Find your task**:
   - Already assigned to you? Continue it.
   - Nothing assigned? Claim from backlog (highest priority first, `[URGENT]` first).
4. **Read task context** (if exists):
   - `refs/designs/F{n}-*.md` - Feature design
   - `refs/plans/F{n}-T{m}-*.md` - Task plan
   - `active/F{n}-*.md` - Feature working context
5. **State your task** before starting work

---

## Multi-Agent Workflow

### Your Identity

Identify yourself as `#yourname` consistently in:

- BACKLOG.md task assignments
- HANDOFF.md entries
- active/ file updates

### WIP Limit

**You may only have 1 task in_progress at a time.**

Before claiming a new task, verify:

- [ ] I have NO current task in_progress
- [ ] My previous task is `done`, `review`, or `blocked`
- [ ] If blocked, I documented it and am NOT claiming another

> **Violation**: If you have a task in_progress, you MUST complete it before claiming another.

### Claiming Tasks (Pull)

1. Read BACKLOG.md - Find unclaimed tasks (no #agent)
2. Pick highest priority:
   - `[URGENT]` items first
   - Then top-to-bottom order
3. Update BACKLOG.md: Add `#yourname`, change to `in_progress`
4. Update HANDOFF.md: Add entry to In Progress
5. Create/update context files as needed
6. Begin work

### Completing a Task

**Self-Check** - Before marking `review`:

- [ ] Task works as described
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
6. **Report to user**: Summarize what was done and request review
7. **END SESSION** - Do NOT automatically claim next task

> **One session = One task.** After completing a task, mark `review` and end the session.
> The task becomes `done` only after user review.

> **Note**: For agent teams *within* a single plan (parallel execution or cross-verification), see [Agent Teams](#agent-teams) under Plan Mode Rule.

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

## Context Compaction Recovery

When context compaction occurs (you notice memory loss or conversation reset):

1. **Re-read essential files** in order:

   - `INSTRUCTION.md` - Restore your guidelines
   - `BACKLOG.md` - Find your assigned task
   - `HANDOFF.md` - Current work status
   - `active/F{n}-*.md` - Your working context (most important)

2. **Restore your state**:

   - Identify yourself as the same `#agent-name`
   - Continue the task you were working on
   - Do NOT claim a new task

3. **Verify before continuing**:
   - [ ] I know which task I was working on
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

When writing plan files, always fill in the Sprint Context section of the `refs/plans/F{n}-T{m}-*.md` template.

### Agent Teams

When writing a plan, **evaluate whether agent teams would improve speed or quality**.

**Use agent teams when:**

For speed:
- 2+ sub-tasks are independent of each other
- Roles are clearly separable (e.g., frontend/backend, research/implementation)
- Parallel execution would meaningfully reduce total time

For quality:
- Implementation and testing benefit from independent perspectives (one agent implements, another writes tests without seeing implementation)
- Cross-verification would catch issues a single agent might miss
- Multiple approaches worth exploring in parallel before choosing

**Document in plan file:**

| Item | Description |
|------|-------------|
| **Team composition** | Agent names, roles, and assigned sub-tasks |
| **Dependencies** | Which tasks block others (use `blockedBy` / `blocks`) |
| **Merge point** | When and how team results are integrated |

**Do NOT use agent teams when:**

- All sub-tasks have sequential dependencies
- Task is simple enough that coordination overhead exceeds benefit
- Single-perspective work is sufficient (straightforward implementation)

---

## Core Principles

1. **Small, Fast Feedback Loops** - Complete tasks incrementally, verify often
2. **Document as You Go** - Keep HANDOFF.md and active/ current
3. **Respect WIP Limits** - One task at a time per agent
4. **Ask Before Deciding** - Unclear? Ask user before making big decisions
