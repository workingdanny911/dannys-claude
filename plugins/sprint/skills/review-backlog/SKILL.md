---
name: review-backlog
description: "Review completed Task or Feature deliverables. Uses type-specific checklists (coding/docs/ideation/general) for quality review. Two modes: default (creates improvement Tasks) and immediate-fix (fixes issues directly). Triggers: 'review task', 'review feature', 'review backlog'"
---

# Sprint Review Backlog Skill

Systematically review completed Task or Feature deliverables, identify areas for improvement, and connect to next actions.

## When to Use

- Immediately after a Task or Feature is completed
- When quality review of code/docs/design is needed
- Before moving to the next Task for checkpoint

## Prerequisites

This skill operates in a sprint folder containing:
- `BACKLOG.md` - Backlog items
- `HANDOFF.md` - Current progress status
- `INSTRUCTION.md` - Agent guidelines
- `refs/` - Reference documents

---

## Execution Modes

This skill supports two modes:

| Aspect | Default Mode | Immediate-Fix Mode |
|--------|-------------|-------------------|
| **When** | Manual review, post-completion | Called from `/sprint:work-on-feature` R&R step |
| **Trigger** | User runs `/sprint:review-backlog` | R&R Agent selects "immediate-fix" when prompted |
| **Output** | New improvement Tasks in BACKLOG.md | Issues fixed directly in code |
| **Post-review** | Tasks for next session | R&R Agent reports fixes to Lead |
| **Sprint files** | Updates BACKLOG.md with Tasks | Does NOT touch sprint files (Lead handles) |

**Mode selection:**
After Step 4 (Report Results), ask:

```
How would you like to handle the findings?
1. Create improvement Tasks (default) — adds Tasks to BACKLOG.md for next session
2. Fix issues directly (immediate-fix) — fix all issues now in this session
```

If the agent is running as part of `/sprint:work-on-feature`, it should select option 2.

---

## Workflow

### Step 1: Understand Sprint Context

**Required files to read:**

1. `BACKLOG.md` - Check completed items
2. `HANDOFF.md` - Check progress status

**After identifying target, read related files:**

| Target | Files to Read |
|--------|---------------|
| Feature | `refs/designs/F{n}-*`, `active/F{n}-*` (contains decisions), `refs/archive/F{n}-*` (if prior Feature) |
| Task | `refs/plans/F{n}-T{m}-*`, related Feature files |

**Sprint-wide (if needed):**
- `refs/decisions/_sprint.md`
- `refs/lessons/_sprint.md`

**Report to user:**
```
Recently completed items:
- T1.2: Login API (done)
- T1.3: Signup API (done)
- F2: Dashboard (done)

What would you like to review?
1. Specific Task
2. Entire Feature
```

---

### Step 2: Identify Review Target

Collect information about the user's selected item:

1. **Check type** - `coding | docs | ideation | general` from BACKLOG.md
2. **Check completion criteria** - Originally defined success criteria
3. **Collect related deliverables** - Code, documents, designs, etc.

---

### Step 3: Apply Type-Specific Checklist

> **Note:** Checklists are minimum standards. Apply additional criteria based on project characteristics.

**Load checklist based on type:**

| Type | Checklist |
|------|-----------|
| coding | `assets/coding/checklist.md` |
| docs | `assets/docs/checklist.md` |
| ideation | `assets/ideation/checklist.md` |
| general | `assets/general/checklist.md` |

**Perform review:**
- Check each checklist item one by one
- Record pass/fail for each item
- Provide detailed explanation for failed items

#### Agent Teams for Review

Consider using agent teams when:

- **Large scope** — Entire Feature or multiple Tasks to review
- **Critical deliverable** — High-risk work where thorough review matters (security, data integrity, core business logic)
- **Other cases** — When deeper or multi-perspective review would add value

**Always propose to the user and get approval before spawning agent teams.**

Parallelization strategies:

| Strategy | Description | Example |
|----------|-------------|---------|
| **By aspect** | Each agent reviews a different quality dimension | functionality, security, performance, code quality |
| **By target** | Each agent reviews a different Task or component | Agent A: T1.1~T1.2, Agent B: T1.3~T1.4 |
| **Cross-verification** | A separate agent validates the primary reviewer's findings | Reduces false positives and missed issues |

After parallel review, **merge results into a single report** in Step 4.

---

### Step 4: Organize Review Results

Categorize findings:

#### Classification Criteria

| Category | Description | Examples |
|----------|-------------|----------|
| 🔴 **Critical** | Immediate fix required, functional/security issues. **Failure to meet goals or acceptance criteria is always Critical.** | Goal not met, acceptance criteria failed, bugs, security vulnerabilities, data loss risk |
| 🟡 **Improvement** | Would be better if improved, quality enhancement | Refactoring candidates, performance improvements, readability |
| 🟢 **Minor** | Minor improvements | Naming, comments, formatting |
| 💡 **Suggestion** | Future considerations | New feature ideas, technical debt |

**Report results to user:**
```
## Review Results: [Item name]

### 🔴 Critical (N items)
1. [Issue]: [Description]
   - Location: [File/location]
   - Impact: [Scope of impact]

### 🟡 Improvement (N items)
1. [Improvement]: [Description]
   - Current: [Current state]
   - Suggested: [Improvement direction]

### 🟢 Minor (N items)
- [Items...]

### 💡 Suggestion (N items)
- [Items...]

---
Would you like to create an improvement plan for Critical/Improvement items?
```

---

### Step 5: Handle Findings

#### Mode A: Default — Create Improvement Tasks

> **Enter Plan Mode if Critical or Improvement items exist and user agrees.**

```
There are items that need improvement.
Entering Plan Mode to create an improvement plan.
```

**Content to write in Plan Mode:**

```markdown
# [Item Name] Improvement Plan

> This plan will be executed in the next session via `@INSTRUCTION.md`.
> Do not start improvement work immediately after plan approval.

## Review Summary
- Review target: [Task/Feature name]
- Issues found: Critical N, Improvement N

## Improvement Tasks

### Task 1: [Improvement item]
- Issue: [Current problem]
- Solution: [Specific solution]
- Scope: [Files/areas to modify]
- Completion criteria: [How to know it's done]

### Task 2: [Improvement item]
...

## Priority Order
1. [What to do first]
2. [Next...]

## Risks
- [Things to watch out for during improvement]

## Estimated Effort
- [Expected time/complexity]
```

**Wait for user approval.**

> **CRITICAL: In default mode, this skill only handles review and planning. It does NOT perform actual improvement work.**
>
> When the user approves the Plan:
> 1. Update BACKLOG.md (Step 6A)
> 2. **End the skill**

#### Mode B: Immediate-Fix — Fix Issues Directly

> **Fix all Critical, Improvement, and Minor issues in this session.**

1. For each issue (Critical first, then Improvement, then Minor):
   - Identify the file and location
   - Apply the fix
   - Verify the fix is correct
2. Run tests if applicable (coding type)
3. Report results:

```
## Immediate-Fix Results

Fixed:
- 🔴 Critical: N/N items fixed
- 🟡 Improvement: N/N items fixed
- 🟢 Minor: N/N items fixed
- 💡 Suggestion: N items (skipped — future consideration)

Unfixable (if any):
- [Issue]: [Why it cannot be fixed]

Files modified:
- [list of files]
```

> **In immediate-fix mode, do NOT modify sprint files (BACKLOG.md, HANDOFF.md, active/).
> The Lead (orchestrator) handles sprint file updates.**

---

### Step 6: Post-Action Updates

#### Step 6A: Default Mode — Post-Approval Updates

> **IMPORTANT: After user approval, only update files and end the skill. Do not start improvement work.**

##### 6A.1 Update BACKLOG.md

**Add improvement Tasks:**
```markdown
- [x] T1.2: Login API `done`
- [ ] T1.4: Fix review issues (T1.2) `backlog`  ← newly added
  - [ ] T1.4.1: [Critical improvement 1]
  - [ ] T1.4.2: [Improvement 1]
```

**Reopen Feature (if Feature was in completed state):**
```markdown
- [ ] F1: Login System  ← changed from [x] to [ ]
```

##### 6A.2 Update HANDOFF.md

Add to `## Context for Next Session`:
```markdown
**Review results to address:**
- [Item name] review found N improvement items
- Improvement Task: T{n}.{m}
- Work from Plan file - no Plan Mode needed
```

#### Step 6B: Immediate-Fix Mode — No Sprint File Updates

In immediate-fix mode, the skill ends after fixing issues and reporting results.
Sprint file updates are handled by the Lead (orchestrator from `/sprint:work-on-feature`).

**End the skill.**

---

### Step 7: Completion Report

#### Default Mode:

```
[Item name] review complete.

Review results:
- 🔴 Critical: N items
- 🟡 Improvement: N items
- 🟢 Minor: N items
- 💡 Suggestion: N items

Updated files:
- BACKLOG.md - Improvement Tasks added
- HANDOFF.md - Status reflected

Call @INSTRUCTION.md in your next session to start improvement work.
```

#### Immediate-Fix Mode:

```
[Item name] review and fix complete.

Review results:
- 🔴 Critical: N found, N fixed
- 🟡 Improvement: N found, N fixed
- 🟢 Minor: N found, N fixed
- 💡 Suggestion: N items (noted)

Files modified:
- [list]

[If unfixable issues exist:]
⚠️ Unfixable issues:
- [issue and reason]
```

---

## Key Principles

- **Type-specific checklists** — Different criteria for coding/docs/ideation/general
- **Classification and prioritization** — Categorize findings by severity
- **Two execution modes** — Default (create Tasks) for manual workflows, immediate-fix for automated orchestration
- **Default mode: Plan-based** — Planned improvements, not ad-hoc fixes; create improvement Tasks
- **Immediate-fix mode: Direct action** — Fix all fixable issues in-session; no sprint file modifications
- **Reopen Feature** — Reopen if Feature was in completed state (default mode only)

---

## Related Skills

- `/sprint:init` - Sprint initialization
- `/sprint:add-backlog` - Add backlog items
- `/sprint:plan-backlog` - Design items in detail
- `/sprint:review-work` - Same-session review, improve, and mark done
- `@INSTRUCTION.md` - Execute improvement work

---

## Example Usage

**User:** "Review T1.2"

**Claude:**
1. Understand sprint context (check T1.2 in BACKLOG.md)
2. Check T1.2 type (coding)
3. Load coding checklist
4. Perform systematic review
5. Categorize and report results
6. (If issues found) Get user confirmation, enter Plan Mode
7. Create improvement plan
8. Wait for user approval
9. After approval, add improvement Tasks to BACKLOG.md
10. Report completion
