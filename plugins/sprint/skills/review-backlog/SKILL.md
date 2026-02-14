---
name: review-backlog
description: "Review completed Task or Feature deliverables. Uses type-specific checklists (coding/docs/ideation/general) for quality review. If issues found, creates improvement plan in Plan mode and adds improvement Tasks to BACKLOG.md. Triggers: 'review task', 'review feature', 'review backlog'"
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

## Workflow

### Step 1: Understand Sprint Context

**Required files to read:**

1. `BACKLOG.md` - Check completed items
2. `HANDOFF.md` - Check progress status

**After identifying target, read related files:**

| Target | Files to Read |
|--------|---------------|
| Feature | `refs/designs/F{n}-*`, `refs/decisions/F{n}-*`, `active/F{n}-*` |
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
| 🔴 **Critical** | Immediate fix required, functional/security issues | Bugs, security vulnerabilities, data loss risk |
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

### Step 5: Create Improvement Plan (When Issues Found)

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

> **CRITICAL: This skill only handles review and planning. It does NOT perform actual improvement work.**
>
> When the user approves the Plan:
> 1. Update BACKLOG.md
> 2. **End the skill**
>
> Do NOT say "Plan approved. Starting improvement work now." and begin work.
> Improvement work happens in the next session via `@INSTRUCTION.md`.

---

### Step 6: Post-Approval Updates

> **IMPORTANT: After user approval, only update files and end the skill. Do not start improvement work.**

#### 6.1 Update BACKLOG.md

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

#### 6.2 Update HANDOFF.md

Add to `## Context for Next Session`:
```markdown
**Review results to address:**
- [Item name] review found N improvement items
- Improvement Task: T{n}.{m}
- Work from Plan file - no Plan Mode needed
```

---

### Step 7: Completion Report

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

---

## Key Principles

- **Type-specific checklists** - Different criteria for coding/docs/ideation/general
- **Classification and prioritization** - Categorize findings by severity
- **Plan-based improvements** - Planned improvements, not ad-hoc fixes
- **Add as new Tasks** - Create improvement Tasks instead of reopening existing ones
- **Reopen Feature** - Reopen if Feature was in completed state
- **Plan file reference required** - Always reference generated Plan file during improvement work

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
