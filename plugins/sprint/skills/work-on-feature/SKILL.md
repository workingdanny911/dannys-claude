---
name: work-on-feature
description: "Automatically execute all Tasks in a Feature. Spawns Worker agents with matched personas, runs review-work, verifies with thorn, and handles Review & Refactor. Triggers: 'work on feature', 'feature 진행', 'feature 실행', '피처 진행', 'run feature'"
---

# Work on Feature

Automatically execute all Tasks in a Feature — spawning Worker agents, running reviews, verifying quality, and recording lessons.

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

**Batch 1** (parallel)
| Task | Persona | Type | Plan |
|------|---------|------|------|
| T{n}.1: {name} | {persona} | {type} | {plan path or "none"} |
| T{n}.2: {name} | {persona} | {type} | {plan path or "none"} |

**Batch 2** (after Batch 1)
| Task | Persona | Type | Plan |
|------|---------|------|------|
| T{n}.3: {name} | {persona} | {type} | {plan path or "none"} |

**Review & Refactor**
| T{n}.4: Review & Refactor F{n} | thorn | review | (auto) |

---
Proceed? You can modify persona assignments or batch grouping.
```

**Wait for user approval.** User may:
- Change persona assignments
- Force sequential execution
- Exclude specific Tasks

---

### Step 4: Batch Loop

For each batch, for each Task in the batch:

#### 4a: Update Sprint Files (Pre-Work)

Update BACKLOG.md: Task status → `in_progress`
Update HANDOFF.md: Add to In Progress table
Create/update `active/F{n}-*.md` if needed

#### 4b: Spawn Worker Agent

Use the `Agent` tool:

```
Agent({
  name: "worker-T{f}.{t}",
  description: "Sprint Task T{f}.{t}",
  prompt: <see Worker Agent Prompt below>,
  mode: "auto"
})
```

**Worker Agent Prompt Construction:**

```
You are {persona_name}, working on a sprint Task.

## Your Persona
{content of personas/{name}.md}

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
1. Execute the Task following your persona's style
2. When complete, run /sprint:review-work
3. After review-work produces findings, report the FULL findings to me (the lead)
   - Include all categories: 🔴 Critical, 🟡 Improvement, 🟢 Minor, 💡 Suggestion
   - Do NOT select or fix items yourself — wait for my instructions
4. Report the list of files you created or modified

## Sprint File Rules
- Do NOT modify BACKLOG.md, HANDOFF.md, or active/ files
- Only work on implementation code and tests
```

#### 4c: Receive Worker Report & Send Fix Instructions

Worker reports back with:
- review-work findings (categorized)
- List of modified files

Lead applies auto-selection policy:

| Category | Action |
|----------|--------|
| 🔴 Critical | **Fix** |
| 🟡 Improvement | **Fix** |
| 🟢 Minor | **Fix** |
| 💡 Suggestion | **Skip** |

Send fix instructions via `SendMessage`:

```
SendMessage({
  to: "worker-T{f}.{t}",
  content: "Fix the following items from your review:

  🔴 Critical: all
  🟡 Improvement: all
  🟢 Minor: all
  💡 Suggestion: skip

  After fixing, report completion with updated file list."
})
```

If no issues found: skip to Step 4e.

#### 4d: Receive Fix Completion

Worker reports fixes applied + updated file list.

#### 4e: Spawn Verifier Agent

Use the `Agent` tool:

```
Agent({
  name: "verifier-T{f}.{t}",
  description: "Verify Task T{f}.{t}",
  prompt: <see Verifier Agent Prompt below>,
  mode: "auto"
})
```

**Verifier Agent Prompt Construction:**

```
You are Thorn, an uncompromising code reviewer.

## Your Persona
{content of personas/thorn.md}

## Verification Target
- Task: T{f}.{t}: {task name}
- Feature: F{n}: {feature name}
- Type: {coding/docs/ideation/general}

## Files to Verify
{list of files from Worker Agent report}

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

### 4. Report
Report to me (the lead):
- Verification status: PASS or FAIL
- Issues found and fixed (if any)
- Issues found but NOT fixable (if any — explain why)
- Final file list after your fixes

If you cannot fix an issue, clearly state why and mark as FAIL.
```

#### 4f: Process Verifier Result

**If PASS:**
- Update BACKLOG.md: Task `[x]` `done`
- Update HANDOFF.md: Move to Recently Done
- Update `active/F{n}-*.md` with completion notes
- Continue to 4g

**If FAIL (unfixable issues):**
- **Stop immediately.** Do not proceed to next Task.
- Report to user:
  ```
  ❌ T{f}.{t} verification failed — unfixable issues:
  - {issue description}

  Task remains in `in_progress`. Please resolve and re-run /sprint:work-on-feature F{n}.
  ```

#### 4g: Learning Loop

After successful Task completion:

1. Check Verifier's report for patterns (repeated issues across Tasks)
2. If patterns found, append to `refs/lessons/F{n}-lessons.md`:

```markdown
## Lesson from T{f}.{t} ({date})

**Pattern**: {description of repeated issue}
**Fix applied**: {what was done}
**Prevention**: {how to avoid in future Tasks}
```

3. These lessons are included in subsequent Worker Agent prompts (Step 4b)

#### 4h: Report to User

One-line summary:

```
✓ T{f}.{t} done ({persona}) — {N} review fixes, {M} verification fixes
```

#### 4i: Parallel Batch Completion

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

#### 5b: Spawn R&R Agent

```
Agent({
  name: "reviewer-F{n}",
  description: "Review & Refactor F{n}",
  prompt: <see R&R Agent Prompt below>,
  mode: "auto"
})
```

**R&R Agent Prompt Construction:**

```
You are Thorn, performing a comprehensive Feature audit.

## Your Persona
{content of personas/thorn.md}

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
5. After all fixes, report:
   - Total issues found per category
   - All fixes applied
   - Any issues you could NOT fix (with explanation)

### Learning
Record Feature-level lessons:
- Architectural patterns that worked well
- Recurring issues across Tasks
- Suggestions for future Features

Report these lessons to me (the lead).

### Sprint File Rules
- Do NOT modify BACKLOG.md, HANDOFF.md, or active/ files
- Only modify implementation code, tests, and documentation
```

#### 5c: Process R&R Result

1. Record lessons → `refs/lessons/F{n}-lessons.md` (Feature-level section)
2. Update BACKLOG.md: R&R Task → `review` (NOT `done`)
3. Update HANDOFF.md: Move to In Review
4. Update `active/F{n}-*.md` with R&R notes

---

### Step 6: Completion Report

```
## Feature F{n}: {name} — Execution Complete

| Task | Persona | Review Fixes | Verification Fixes | Status |
|------|---------|-------------|-------------------|--------|
| T{n}.1 | {persona} | {N} | {M} | ✓ done |
| T{n}.2 | {persona} | {N} | {M} | ✓ done |
| T{n}.3 R&R | thorn | {N} | — | ⏳ review |

**Lessons recorded**: refs/lessons/F{n}-lessons.md

R&R Task is in `review` status. Please verify and mark done when ready.
```

---

## Error Handling

| Failure Point | Behavior |
|--------------|----------|
| Worker Agent fails to complete Task | Stop. Report failure reason. Task stays `in_progress`. |
| review-work Critical items unresolvable | Stop. Report unresolved items. Task stays `in_progress`. |
| Verifier finds unfixable issues | Stop. Report issues. Task stays `in_progress`. |
| Build/test failures persist | Stop. Report error logs. Task stays `in_progress`. |
| Parallel batch file conflict | Stop. Report conflicting files. |
| Blocked Task encountered (resume) | Stop. Report blocked Task and reason. |

**On any failure:**
```
❌ {Task ID} failed at {stage} — {reason summary}
Task remains in current state. Resolve the issue and re-run:
/sprint:work-on-feature F{n}
```

---

## Key Principles

- **Lead manages sprint files** — Worker and Verifier Agents never touch BACKLOG.md, HANDOFF.md, or active/
- **Fresh Verifier per Task** — No accumulated bias, clean context
- **Lessons feed forward** — Earlier Task lessons improve later Worker prompts
- **Fail fast** — Any unresolvable issue stops the entire flow
- **R&R ends at review** — User makes the final call on Feature quality
- **Parallel when safe** — Only when file overlap is confirmed absent

---

## Related Skills

- `/sprint:review-work` — Same-session review (used by Worker Agents)
- `/sprint:review-backlog` — Comprehensive audit (used by R&R Agent in immediate-fix mode)
- `/sprint:add-backlog` — Add work items
- `/sprint:plan-backlog` — Design Task details
- `/explain:explain` — Feature briefing
- `@INSTRUCTION.md` — Manual session start
