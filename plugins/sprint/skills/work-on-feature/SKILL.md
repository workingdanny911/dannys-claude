---
name: work-on-feature
description: "Automatically execute all Tasks in a Feature. Creates an Agent Team with Worker/Verifier teammates, enables bidirectional communication via SendMessage, and handles Review & Refactor. Triggers: 'work on feature', 'feature 진행', 'feature 실행', '피처 진행', 'run feature'"
---

# Work on Feature

Automatically execute all Tasks in a Feature — creating an Agent Team with Worker and Verifier teammates, coordinating via bidirectional messaging, running reviews, verifying quality, and recording lessons.

## When to Use

- When a Feature has Tasks ready to execute (`backlog` status)
- User wants automated end-to-end Feature execution
- Tasks have been planned (`/sprint:plan-backlog`) or are self-explanatory

## Prerequisites

Sprint folder with:
- `BACKLOG.md` - Feature with Tasks defined
- `HANDOFF.md` - Current status
- `INSTRUCTION.md` - Agent guidelines
- `personas/` - Persona files
- `active/` - Feature context
- `refs/` - Reference documents

---

## Architecture: Agent Teams

This skill uses **Agent Teams** (TeamCreate) instead of standalone Sub-Agents.

```
Lead (you)
├── TeamCreate("feature-F{n}")     ← creates team + shared task list
├── Agent(team_name, name)         ← spawns teammates into the team
├── SendMessage(to: name)          ← bidirectional communication
└── TaskCreate/TaskUpdate          ← shared task board coordination
```

**Why Agent Teams:**
- **Bidirectional messaging** — Lead ↔ Worker ↔ Verifier can communicate freely via SendMessage
- **Shared task board** — All teammates see the same TaskList, claim work, update status
- **Persistent teammates** — Workers stay alive across review cycles (no respawn overhead)
- **Peer collaboration** — Teammates can message each other directly when needed

---

## Workflow

### Step 1: Context Loading

**Read these files:**

| File | Purpose |
|------|---------|
| `BACKLOG.md` | Feature's Task list, statuses, dependencies |
| `refs/designs/F{n}-*.md` | Feature design (goals, type, scope) |
| `refs/plans/F{n}-T{m}-*.md` | Task plans (if exist) |
| `refs/lessons/*.md` | Existing lessons for Worker prompts |
| `personas/*.md` | All persona files (for matching) |
| `active/F{n}-*.md` | Feature context (if exists) |

**Parse Feature Tasks:**
- Extract all Tasks under the target Feature
- Identify the Review & Refactor Task (always last non-merge Task)
- Separate: regular Tasks vs. R&R Task vs. merge Task (worktree mode)

**Resume detection:**
Check Task statuses for resume scenario:

| Status | Action |
|--------|--------|
| `done` | Skip |
| `backlog` | Normal execution |
| `in_progress` | Reset to `backlog`, rework from start |
| `review` | Skip to Verifier Agent (work already done) |
| `blocked` | **Stop immediately.** Report: "T{n}.{m} is blocked. Resolve and re-run." |

---

### Step 2: Briefing (Optional)

Ask the user:

```
This Feature has N Tasks:
- T{n}.1: ...
- T{n}.2: ...
- T{n}.3: Review & Refactor F{n}

Would you like a detailed explanation before proceeding?
1. Yes → /explain briefing
2. No → proceed to execution plan
```

If Yes: invoke `/explain:explain` with Feature design doc and Task list as context.

---

### Step 3: Execution Plan

#### 3a: Persona Matching

For each Task (excluding R&R):

1. Read Task description, type (from Feature Design), and plan (if exists)
2. Read all `personas/*.md` files — check `traits.domain`, `traits.decision_style`
3. Match Task to best persona:

| Signal | Persona Match |
|--------|--------------|
| Task type `coding` + backend keywords (API, database, server) | Check personas with `domain: backend` |
| Task type `coding` + frontend keywords (UI, component, CSS) | Check personas with `domain: frontend` |
| Task type `coding` + fullstack/prototype keywords | Check personas with `domain: fullstack` |
| Task type `coding` + infra/deploy/migration keywords | Check personas with `domain: infra` |
| Task type `ideation` or discussion | Check personas with `domain: discussion` |
| Task type `docs` or `general` | Analyze content, pick closest domain match |

R&R Task always uses `thorn`.

#### 3b: Dependency Analysis

For Tasks with plans (`refs/plans/F{n}-T{m}-*.md`):
1. Read "Files to Modify" section
2. Check file overlap between Tasks
3. Group into batches:

```
Parallel eligibility:
├── Both Tasks have plans with file lists → check overlap
│   ├── No overlap → same batch (parallel)
│   └── Overlap → sequential batches
├── One or both lack plans → sequential (safe default)
└── Explicit dependency noted → sequential
```

For Tasks without plans: always sequential.

#### 3c: Present Execution Plan

```
## Execution Plan for F{n}: {Feature Name}

**Team**: feature-F{n}
**Model**: opus (all teammates)

**Batch 1** (parallel)
| Task | Teammate | Persona | Type | Plan |
|------|----------|---------|------|------|
| T{n}.1: {name} | worker-T{n}.1 | {persona} | {type} | {plan path or "none"} |
| T{n}.2: {name} | worker-T{n}.2 | {persona} | {type} | {plan path or "none"} |

**Batch 2** (after Batch 1)
| Task | Teammate | Persona | Type | Plan |
|------|----------|---------|------|------|
| T{n}.3: {name} | worker-T{n}.3 | {persona} | {type} | {plan path or "none"} |

**Verifier**: verifier-F{n} (thorn, spawned per verification cycle)
**Review & Refactor**: reviewer-F{n} (thorn)

---
Proceed? You can modify persona assignments or batch grouping.
```

**Wait for user approval.** User may:
- Change persona assignments
- Force sequential execution
- Exclude specific Tasks

---

### Step 4: Team Creation & Batch Loop

#### 4a: Create Agent Team

```
TeamCreate({
  team_name: "feature-F{n}",
  description: "Feature F{n}: {feature name} execution team"
})
```

#### 4b: Create Team Tasks

Create tasks in the shared task list for all planned work:

```
TaskCreate({
  title: "T{f}.{t}: {task name}",
  description: "Persona: {persona}, Type: {type}, Plan: {plan path or 'none'}",
  status: "not_started"
})
```

Create tasks for:
- Each regular Task (not_started)
- Each verification task (blocked — unblocked after worker completes)
- R&R task (blocked — unblocked after all regular Tasks done)

#### 4c: Update Sprint Files (Pre-Work)

For each Task in the current batch:
- Update BACKLOG.md: Task status → `in_progress`
- Update HANDOFF.md: Add to In Progress table
- Create/update `active/F{n}-*.md` if needed

#### 4d: Spawn Worker Teammates

For each Task in the current batch, spawn a teammate into the team:

```
Agent({
  name: "worker-T{f}.{t}",
  team_name: "feature-F{n}",
  description: "Sprint Task T{f}.{t}",
  model: "opus",
  prompt: <see Worker Teammate Prompt below>,
  mode: "auto"
})
```

**Spawn all Workers in a batch in parallel** (single message with multiple Agent calls).

**Worker Teammate Prompt Construction:**

```
You are {persona_name}, a teammate in the "feature-F{n}" Agent Team working on a sprint Task.

## Your Persona
{content of personas/{name}.md}

## Team Info
- Team: feature-F{n}
- Your name: worker-T{f}.{t}
- Lead: The agent who spawned you (send messages via SendMessage)
- You can message any teammate by name via SendMessage

## Task Assignment
- Task: T{f}.{t}: {task name}
- Feature: F{n}: {feature name}
- Type: {coding/docs/ideation/general}

## Context
{content of active/F{n}-*.md}

## Feature Design
{content of refs/designs/F{n}-*.md}

## Task Plan
{content of refs/plans/F{n}-T{m}-*.md OR "No plan. Use Feature Design and Task description."}

## Lessons from Previous Tasks
{content of refs/lessons/F{n}-lessons.md if exists, OR "No prior lessons."}

## Instructions
1. Check TaskList to find your assigned task and claim it via TaskUpdate (owner: "worker-T{f}.{t}", status: "in_progress")
2. Execute the Task following your persona's style
3. When implementation is complete, send a completion report to the lead via SendMessage:
   - The complete list of files you created or modified
   - Brief summary of what you implemented
4. Wait for the lead's instructions — the lead will tell you to run review-work
5. When instructed, run /sprint:review-work and send the findings to the lead
6. Wait for the lead's selection — the lead will tell you which items to fix
7. Fix the selected items, then send the updated file list to the lead
8. Wait for the lead's verification result — the lead will spawn a Verifier to check your work
9. If the Verifier contacts you with questions about design intent, respond via SendMessage

## Communication
- **Always use SendMessage** to communicate with the lead or other teammates
- Plain text output is NOT visible to others — you MUST use SendMessage
- When you need help or have questions, message the lead

## Sprint File Rules
- Do NOT modify BACKLOG.md, HANDOFF.md, or active/ files
- Only work on implementation code and tests
```

#### 4e: Lead Directs Review-Work Cycle

**Step 1 — Worker reports implementation complete.** Lead receives file list + summary.

**Step 2 — Lead instructs review-work:**

```
SendMessage({
  to: "worker-T{f}.{t}",
  summary: "Run review-work on T{f}.{t}",
  message: "Implementation looks good. Now run /sprint:review-work on your work and send me the findings."
})
```

**Step 3 — Worker sends review findings.** Lead receives categorized results.

**Step 4 — Lead selects "all" (fix everything including Suggestions):**

```
SendMessage({
  to: "worker-T{f}.{t}",
  summary: "Fix all review items for T{f}.{t}",
  message: "Fix all items: select 'all'. This includes 🔴 Critical, 🟡 Improvement, 🟢 Minor, and 💡 Suggestion.
  After fixing, send me the updated file list."
})
```

**Step 5 — Worker sends fix completion + updated file list.** Proceed to verification (Step 4f).

#### 4f: Spawn Verifier Teammate

Spawn a Verifier into the same team:

```
Agent({
  name: "verifier-T{f}.{t}",
  team_name: "feature-F{n}",
  description: "Verify Task T{f}.{t}",
  model: "opus",
  prompt: <see Verifier Teammate Prompt below>,
  mode: "auto"
})
```

**Verifier Teammate Prompt Construction:**

```
You are Thorn, an uncompromising code reviewer and a teammate in the "feature-F{n}" Agent Team.

## Your Persona
{content of personas/thorn.md}

## Team Info
- Team: feature-F{n}
- Your name: verifier-T{f}.{t}
- Lead: The agent who spawned you (send messages via SendMessage)
- Worker who wrote this code: worker-T{f}.{t}

## Verification Target
- Task: T{f}.{t}: {task name}
- Feature: F{n}: {feature name}
- Type: {coding/docs/ideation/general}

## Files to Verify
{list of files from Worker report}

## Acceptance Criteria
{from Task plan or Feature Design}

## Instructions

### 1. Code Review (Third-Party Perspective)
Review all modified files with fresh eyes. You did NOT write this code.
Apply your review standards: correctness, maintainability, naming, security, test coverage.

### 2. Mechanical Verification
Run these checks and report results:
- Tests: run the project's test suite (or relevant subset)
- Build: verify the project builds without errors
- Type check: run type checker if applicable
- Lint: run linter if applicable

### 3. Fix Issues
If you find issues:
- Fix them directly
- Report what you fixed and why

### 4. Communicate
- If you need clarification about intent, message the Worker directly:
  SendMessage({ to: "worker-T{f}.{t}", message: "..." })
- The Worker can explain their design decisions — use this before making assumptions

### 5. Report
Send your report to the lead via SendMessage:
- Verification status: PASS or FAIL
- Issues found and fixed (if any)
- Issues found but NOT fixable (if any — explain why)
- Final file list after your fixes

If you cannot fix an issue, clearly state why and mark as FAIL.

## Communication
- **Always use SendMessage** to communicate with the lead or other teammates
- You CAN message the Worker directly for clarification — this is encouraged
- Plain text output is NOT visible to others — you MUST use SendMessage
```

#### 4g: Process Verifier Result

**If PASS:**
- Update BACKLOG.md: Task `[x]` `done`
- Update HANDOFF.md: Move to Recently Done
- Update `active/F{n}-*.md` with completion notes
- TaskUpdate: mark verification task as completed
- Continue to 4h

**If FAIL (unfixable issues):**
- **Stop immediately.** Do not proceed to next Task.
- Report to user:
  ```
  ❌ T{f}.{t} verification failed — unfixable issues:
  - {issue description}

  Task remains in `in_progress`. Please resolve and re-run /sprint:work-on-feature F{n}.
  ```

#### 4h: Learning Loop

After successful Task completion:

1. Check Verifier's report for patterns (repeated issues across Tasks)
2. If patterns found, append to `refs/lessons/F{n}-lessons.md`:

```markdown
## Lesson from T{f}.{t} ({date})

**Pattern**: {description of repeated issue}
**Fix applied**: {what was done}
**Prevention**: {how to avoid in future Tasks}
```

3. These lessons are included in subsequent Worker prompts (Step 4d)

#### 4i: Shutdown Completed Workers

After a Worker's Task is fully done (verified + lessons recorded):

```
SendMessage({
  to: "worker-T{f}.{t}",
  message: { type: "shutdown_request" }
})
```

Also shutdown the Verifier:

```
SendMessage({
  to: "verifier-T{f}.{t}",
  message: { type: "shutdown_request" }
})
```

#### 4j: Report to User

One-line summary:

```
✓ T{f}.{t} done ({persona}) — {N} self-review fixes, {M} verification fixes
```

#### 4k: Parallel Batch Completion

When all Tasks in a batch complete:

1. **Conflict detection** (parallel batches only):
   - Check if any Workers/Verifiers modified the same files
   - If conflict detected: **Stop.** Report conflicting files and which Tasks touched them.
2. Proceed to next batch

---

### Step 5: Review & Refactor Task

After all regular Tasks are done:

#### 5a: Update Sprint Files

Update BACKLOG.md: R&R Task → `in_progress`
Update HANDOFF.md: Add to In Progress
TaskUpdate: unblock R&R task

#### 5b: Spawn R&R Teammate

```
Agent({
  name: "reviewer-F{n}",
  team_name: "feature-F{n}",
  description: "Review & Refactor F{n}",
  model: "opus",
  prompt: <see R&R Teammate Prompt below>,
  mode: "auto"
})
```

**R&R Teammate Prompt Construction:**

```
You are Thorn, performing a comprehensive Feature audit as a teammate in the "feature-F{n}" Agent Team.

## Your Persona
{content of personas/thorn.md}

## Team Info
- Team: feature-F{n}
- Your name: reviewer-F{n}
- Lead: The agent who spawned you (send messages via SendMessage)

## Feature Under Review
- Feature: F{n}: {feature name}
- Type: {coding/docs/ideation/general}
- Design: {content of refs/designs/F{n}-*.md}

## Completed Tasks
{list of all Tasks and what they accomplished}

## Instructions

### Run /sprint:review-backlog in immediate-fix mode

1. Invoke /sprint:review-backlog targeting Feature F{n}
2. When the skill asks about mode, choose **immediate-fix mode**
3. Apply the comprehensive checklist against the entire Feature
4. For each issue found: fix it directly
5. After all fixes, send report to the lead via SendMessage:
   - Total issues found per category
   - All fixes applied
   - Any issues you could NOT fix (with explanation)

### Learning
Record Feature-level lessons:
- Architectural patterns that worked well
- Recurring issues across Tasks
- Suggestions for future Features

Send these lessons to the lead via SendMessage.

## Communication
- **Always use SendMessage** to communicate with the lead
- Plain text output is NOT visible to others — you MUST use SendMessage

### Sprint File Rules
- Do NOT modify BACKLOG.md, HANDOFF.md, or active/ files
- Only modify implementation code, tests, and documentation
```

#### 5c: Process R&R Result

1. Record lessons → `refs/lessons/F{n}-lessons.md` (Feature-level section)
2. Update BACKLOG.md: R&R Task → `review` (NOT `done`)
3. Update HANDOFF.md: Move to In Review
4. Update `active/F{n}-*.md` with R&R notes

#### 5d: Shutdown R&R Teammate

```
SendMessage({
  to: "reviewer-F{n}",
  message: { type: "shutdown_request" }
})
```

---

### Step 6: Team Shutdown & Completion Report

#### 6a: Shutdown All Remaining Teammates

Send shutdown to any teammates still alive:

```
SendMessage({
  to: "*",
  message: { type: "shutdown_request" }
})
```

#### 6b: Completion Report

```
## Feature F{n}: {name} — Execution Complete

**Team**: feature-F{n} (shutdown)

| Task | Teammate | Persona | Review Fixes | Verification Fixes | Status |
|------|----------|---------|-------------|-------------------|--------|
| T{n}.1 | worker-T{n}.1 | {persona} | {N} self-review | {M} | ✓ done |
| T{n}.2 | worker-T{n}.2 | {persona} | {N} self-review | {M} | ✓ done |
| T{n}.3 R&R | reviewer-F{n} | thorn | {N} | — | ⏳ review |

**Lessons recorded**: refs/lessons/F{n}-lessons.md

R&R Task is in `review` status. Please verify and mark done when ready.
```

---

## Error Handling

| Failure Point | Behavior |
|--------------|----------|
| Worker teammate fails to complete Task | Stop. Report failure reason. Task stays `in_progress`. |
| Worker cannot resolve self-review items | Stop. Report unresolved items. Task stays `in_progress`. |
| Verifier finds unfixable issues | Stop. Report issues. Task stays `in_progress`. |
| Build/test failures persist | Stop. Report error logs. Task stays `in_progress`. |
| Parallel batch file conflict | Stop. Report conflicting files. |
| Blocked Task encountered (resume) | Stop. Report blocked Task and reason. |
| Teammate becomes unresponsive | Send message asking for status. If no response, report to user. |

**On any failure:**
```
❌ {Task ID} failed at {stage} — {reason summary}
Task remains in current state. Resolve the issue and re-run:
/sprint:work-on-feature F{n}
```

**On failure cleanup:** Shutdown all teammates before stopping:
```
SendMessage({ to: "*", message: { type: "shutdown_request" } })
```

---

## Key Principles

- **Agent Teams, not Sub-Agents** — All agents are teammates in a shared team with bidirectional messaging
- **Lead delegates, decides, and verifies** — Lead assigns work, directs review-work, selects fix scope ("all"), and spawns Verifiers
- **Workers execute** — Workers implement, run review-work when told, fix selected items, and report back
- **Lead manages sprint files** — Worker and Verifier teammates never touch BACKLOG.md, HANDOFF.md, or active/
- **Bidirectional communication** — Workers and Verifiers can message each other and the Lead freely via SendMessage
- **Shared task board** — TaskCreate/TaskUpdate for coordination, visible to all teammates
- **Opus by default** — All teammates use `model: "opus"` for maximum capability
- **Fresh Verifier per Task** — No accumulated bias, clean context
- **Verifier ↔ Worker dialogue** — Verifier can ask Worker for design intent before assuming bugs
- **Lessons feed forward** — Earlier Task lessons improve later Worker prompts
- **Fail fast** — Any unresolvable issue stops the entire flow
- **Clean shutdown** — Always shutdown teammates via SendMessage before stopping
- **R&R ends at review** — User makes the final call on Feature quality
- **Parallel when safe** — Only when file overlap is confirmed absent

---

## Related Skills

- `/sprint:review-work` — Same-session review (used by Worker teammates)
- `/sprint:review-backlog` — Comprehensive audit (used by R&R teammate in immediate-fix mode)
- `/sprint:add-backlog` — Add work items
- `/sprint:plan-backlog` — Design Task details
- `/explain:explain` — Feature briefing
- `@INSTRUCTION.md` — Manual session start
