---
name: review-work
description: "Review work in the current session after an agent marks a task as review. Applies type-specific criteria (coding/design/docs/general), reports findings, user selects improvements, enters Plan Mode, then executes improvements and marks task done. Triggers: 'review work', '작업 리뷰', '리뷰해줘'"
---

# Sprint Review Work Skill

Review a task in `review` status, identify improvements, and execute selected fixes — all in the same session.

## When to Use

- After an agent marks a task as `review` and reports to the user
- Called in the **same session** where the work was just completed
- Quality gate between `review` → `done` transition

## Prerequisites

This skill operates in a sprint folder containing:
- `BACKLOG.md` - Backlog items
- `HANDOFF.md` - Current progress status
- `active/` - Feature working contexts
- `refs/` - Reference documents

---

## Key Difference from `/sprint:review-backlog`

| Aspect | review-backlog | review-work |
|--------|---------------|-------------|
| **When** | Any time, post-completion | Same session, right after agent reports |
| **Scope** | Comprehensive audit checklist | Focused review criteria |
| **Output** | New improvement Tasks in BACKLOG | Selected improvements executed immediately |
| **Execution** | Next session via `@INSTRUCTION.md` | Same session after plan approval |
| **Result** | Task stays, new Tasks added | Reviewed task marked `done` |

---

## Workflow

### Step 1: Identify Review Target (Current Session Context)

This skill is called in the **same session** where the agent just completed work and marked it as `review`.
Use the current conversation context to identify the review target — no need to scan BACKLOG.md.

- Extract Task ID, Feature, and work summary from the agent's completion report
- If unclear, ask the user: "Which task should I review?"

---

### Step 2: Gather Context

Leverage information already in the session. Read additional files as needed:

| Source | Purpose |
|--------|---------|
| `active/F{n}-*.md` | Work notes, modified files list |
| `refs/plans/F{n}-T{m}-*.md` | Original plan (intent vs. outcome) |
| `refs/designs/F{n}-*.md` | Feature design (goals, type) |

**Determine task type** from the Feature's Design doc:
- `coding` | `design` | `docs` | `general`

**For `coding` tasks**, also read:
- Actual source files mentioned in active context
- Test files related to the implementation

**For `design` tasks**, also read:
- Design documents produced
- Decision records created

---

### Step 3: Apply Review Criteria

**Load criteria based on type:**

| Type | Criteria File |
|------|---------------|
| coding | `assets/coding/criteria.md` |
| design | `assets/design/criteria.md` |
| docs | `assets/docs/criteria.md` |
| general | `assets/general/criteria.md` |

> **Note:** These are focused review criteria, not exhaustive checklists.
> Review what was actually delivered. Flag real issues, not hypothetical concerns.

---

### Step 4: Report Findings & User Selection

**Categorize findings:**

| Category | Description |
|----------|-------------|
| 🔴 **Critical** | Must fix — bugs, security issues, broken functionality |
| 🟡 **Improvement** | Should fix — readability, maintainability, quality |
| 🟢 **Minor** | Nice to fix — naming, formatting, small cleanups |
| 💡 **Suggestion** | Future consideration only — not for this session |

**Report format:**

```
## Review: T{n}.{m}: [Task name]

### Summary
[1-2 sentence summary of what was done and overall quality assessment]

### 🔴 Critical (N items)
1. [Issue]: [Description]
   - Location: [File/location]
   - Impact: [Why this matters]

### 🟡 Improvement (N items)
1. [Issue]: [Description]
   - Current: [Current state]
   - Suggested: [What to improve]

### 🟢 Minor (N items)
1. [Issue]: [Brief description]

### 💡 Suggestion (N items)
- [Suggestion for future work]

---
Which items would you like to fix before marking done?
- Enter numbers (e.g., "all critical, improvement 1, 3")
- Enter "none" to mark done as-is
- Enter "all" to fix everything except suggestions
```

**If no issues found:**
```
## Review: T{n}.{m}: [Task name]

### Summary
[Summary of work done]

No issues found. Task meets all review criteria.
Mark as done?
```

---

### Step 5: Plan Improvements (When Items Selected)

> **Enter Plan Mode when user selects improvements to fix.**

```
Creating improvement plan for selected items.
Entering Plan Mode.
```

**Plan file content:**

```markdown
# T{n}.{m}: [Task Name] - Review Improvements

> Execute improvements and mark task as done.

## Sprint Context

| Key | Value |
|-----|-------|
| Sprint | `{sprint-absolute-path}` |
| Feature | `F{n}: {feature-name}` |
| Task | `T{n}.{m}: {task-name}` |

**Required reads after context clear:**
1. `{sprint-path}/BACKLOG.md`
2. `{sprint-path}/HANDOFF.md`
3. `{sprint-path}/active/F{n}-*.md`

## Review Summary
- Reviewed: T{n}.{m}: [task name]
- Critical: N, Improvement: N, Minor: N
- Selected for improvement: [list]

## Improvements

### 1. [Improvement title]
- **Issue**: [What's wrong]
- **Fix**: [Specific steps]
- **Files**: [Files to modify]

### 2. [Improvement title]
...

## Post-Improvement Steps

1. Verify all improvements are applied
2. Run tests (if coding type)
3. Update BACKLOG.md: `[ ] T{n}.{m}: [name] \`review\`` → `[x] T{n}.{m}: [name] \`done\``
4. Update HANDOFF.md: Move from In Review → Recently Done
5. Update `active/F{n}-*.md` with review completion notes
6. Check if Feature is now complete (all Tasks done)
   - If yes: mark Feature `[x]` in BACKLOG.md
```

**Wait for user approval.**

---

### Step 6: Execute Improvements

> **After plan approval, execute immediately (unlike review-backlog).**

1. Apply each improvement from the plan
2. Verify improvements are correct
3. Run tests if applicable (coding type)

---

### Step 7: Mark Done & Update Files

#### 7.1 Update BACKLOG.md

```markdown
# Before
- [ ] T1.2: Login API `review`

# After
- [x] T1.2: Login API `done`
```

If all Tasks in the Feature are `done`:
```markdown
- [x] F1: User Authentication
```

#### 7.2 Update HANDOFF.md

Move task from **In Review** to **Recently Done**.

#### 7.3 Update active/F{n}-*.md

Add review completion notes.

---

### Step 8: Completion Report

```
T{n}.{m}: [Task name] review complete.

Review results:
- 🔴 Critical: N items (N fixed)
- 🟡 Improvement: N items (N fixed)
- 🟢 Minor: N items (N fixed)
- 💡 Suggestion: N items (noted)

Improvements applied:
- [List of applied improvements]

Updated files:
- BACKLOG.md - Task marked done
- HANDOFF.md - Moved to Recently Done
- active/F{n}-*.md - Review notes added
```

---

## Shortcut: No Issues / "none" Selected

When no issues found or user selects "none":
1. Skip Plan Mode entirely
2. Go directly to Step 7 (Mark Done & Update Files)
3. Report completion (Step 8)

---

## Key Principles

- **Same-session execution** — Improvements applied immediately, not deferred
- **Focused, not exhaustive** — Concise criteria; this is not an audit
- **User controls scope** — User selects which improvements to pursue
- **Plan Mode for improvements only** — Skip when no improvements needed
- **Task transitions to done** — The reviewed task is marked done in this session

---

## Related Skills

- `/sprint:review-backlog` — Comprehensive audit with new Tasks for next session
- `/sprint:plan-backlog` — Design items in detail
- `/sprint:add-backlog` — Add backlog items
- `@INSTRUCTION.md` — Start work sessions
