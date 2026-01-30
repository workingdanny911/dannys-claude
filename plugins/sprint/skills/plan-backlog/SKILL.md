---
name: plan-backlog
description: "Design Feature or Task in detail within a sprint. Refines backlog items through brainstorming, creates implementation plan in Plan mode, and adds Sub-tasks to BACKLOG.md upon approval. Triggers: 'plan task', 'plan feature', 'plan backlog'"
---

# Sprint Plan Backlog Skill

Design Feature or Task in detail and break down into actionable Sub-tasks.

## When to Use

- When a sprint created by `/sprint:init` exists
- Before starting a Feature or Task that needs detailed design
- When breaking down a large Task into smaller Sub-tasks

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

1. `BACKLOG.md` - Check current backlog items
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
Current backlog:
- F1: [Feature name] (N tasks)
- F2: [Feature name] (N tasks)

Which item would you like to design in detail?
1. Entire Feature
2. Specific Task
```

---

### Step 2: Brainstorming (Inline)

> **No documents are created in this step - conversation only.**

Refine implementation approach for the selected item through brainstorming.

#### 2.1 Understanding the Item

- One question at a time
- Multiple choice when possible (provide options)
- Focus on implementation approach, technical considerations, dependencies

**Example questions:**
```
Before designing [Task name], I need to clarify a few things.

What is the main implementation approach for this Task?
1. [Option A] - description
2. [Option B] - description
3. [Option C] - description
4. Enter custom answer
```

#### 2.2 Exploring Approaches

- Suggest 2-3 different approaches
- Explain pros/cons of each
- Present recommended option first with reasoning

**Suggestion format:**
```
Here are suggested approaches for [item name]:

**Recommended: [Approach A]**
- Pros: ...
- Cons: ...
- Why recommended: ...

**Alternative 1: [Approach B]**
- Pros: ...
- Cons: ...

Which approach would you prefer?
```

#### 2.3 Design Validation

Present understanding in 200-300 word chunks, confirming each section:

```
[Section Title]

[200-300 words of explanation]

Does this look correct so far?
```

**Sections to cover:**
1. Item overview and goals
2. Sub-task breakdown
3. Technical considerations (if applicable)
4. Success criteria and completion conditions
5. Dependencies and risks

---

### Step 3: Enter Plan Mode

After brainstorming is complete, **enter Plan Mode**.

```
Brainstorming complete.
Now entering Plan Mode to write the detailed plan.
```

**Content to write in Plan Mode:**

```markdown
# F{n}-T{m}: [Item Name] Implementation Plan

> This plan will be executed in the next session via `@INSTRUCTION.md`.
> Do not start work immediately after plan approval.

## Overview
- Goal: ...
- Scope: ...
- Type: coding | docs | ideation | general

## Sub-tasks

### T{n}.{m}.1: [Sub-task name]
- Purpose: ...
- Details: ...
- Completion criteria: ...

### T{n}.{m}.2: [Sub-task name]
...

## Technical Considerations
(if applicable)

## Dependencies
- Prerequisites: ...
- Required resources: ...

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| ... | ... | ... |
```

**Wait for user approval.**

> **CRITICAL: This skill only handles design. It does NOT perform actual implementation.**
>
> When the user approves the Plan:
> 1. Update BACKLOG.md and refs/plans/
> 2. **End the skill**
>
> Do NOT say "Plan approved. Starting implementation now." and begin work.
> Actual implementation happens in the next session via `@INSTRUCTION.md`.

---

### Step 4: Post-Approval Updates

> **IMPORTANT: After user approval, only update files and end the skill. Do not start implementation.**

When user approves the Plan:

#### 4.1 Update BACKLOG.md

**Before:**
```markdown
- [ ] T1.1: Login API `backlog`
```

**After:**
```markdown
- [ ] T1.1: Login API `backlog`
  - [ ] T1.1.1: Define request/response schema
  - [ ] T1.1.2: Implement endpoint
  - [ ] T1.1.3: Add validation
```

#### 4.2 Create Plan Document

Create `refs/plans/F{n}-T{m}-[name].md`

#### 4.3 Update refs/decisions (if needed)

Record decisions made during brainstorming:
- Feature-related → `refs/decisions/F{n}-[name].md`
- Sprint-wide → `refs/decisions/_sprint.md`

#### 4.4 Update HANDOFF.md (if needed)

Add to `## Context for Next Session`:
```markdown
**Planning complete:**
- [Item name] detailed design complete
- Plan document: refs/plans/F{n}-T{m}-[name].md
- Work from Plan file - no Plan Mode needed
```

---

### Step 5: Completion Report

```
[Item name] design complete.

Updated files:
- BACKLOG.md - Sub-tasks added
- refs/plans/F{n}-T{m}-[name].md - Detailed plan

Call @INSTRUCTION.md in your next session to start working on the designed item.
```

---

## Key Principles

- **Brainstorming through conversation** - No separate brainstorming documents
- **Plan Mode for detailed design only** - File updates executed directly without Plan Mode
- **Modify only the target item** - Don't touch other items
- **One question at a time** - Don't overwhelm the user
- **YAGNI principle** - Exclude unnecessary features from design
- **Validate Task size** - Ensure each Sub-task is completable in a single session

---

## Related Skills

- `/sprint:init` - Sprint initialization (prerequisite for this skill)
- `/sprint:add-backlog` - Add backlog items (item creation)
- `/sprint:review-backlog` - Review completed items
- `@INSTRUCTION.md` - Start actual work after design complete

---

## Example Usage

**User:** "Plan task T1.2"

**Claude:**
1. Understand sprint context (read BACKLOG.md, HANDOFF.md)
2. Read T1.2 related files (refs/designs/, refs/plans/)
3. Start brainstorming (Q&A iteration)
4. Validate understanding section by section
5. Enter Plan Mode, write plan
6. Wait for user approval
7. After approval, add Sub-tasks to BACKLOG.md
8. Create plan document in refs/plans/
9. Report completion
