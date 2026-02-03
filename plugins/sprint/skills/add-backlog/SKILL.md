---
name: add-backlog
description: Add backlog items to an existing sprint through guided brainstorming and planning. Automatically detects sprint context or asks for sprint location. Includes brainstorming phase, plan mode for task design, and ensures tasks are sized for single Claude Code sessions. Triggers include "add backlog", "new feature", "add task", "백로그 추가", "기능 추가", "태스크 추가".
---

# Add Backlog Items

Add work items to a sprint through guided brainstorming and structured planning.

## Overview

This skill guides you through:
1. **Brainstorming** - Understand what to build
2. **Planning** - Design Feature/Task structure
3. **Adding** - Update BACKLOG.md with new items

**Key constraint**: Each Task must be completable in a single Claude Code session.

---

## Workflow

### Phase 1: Find Sprint

1. Check current directory for sprint files (BACKLOG.md, HANDOFF.md)
2. If found, confirm: "Add to this sprint?"
3. If not found, ask: "Which sprint? (path or name)"

### Phase 2: Brainstorming (Built-in)

Use conversational discovery to understand what to build.

**Principles:**
- One question at a time
- Multiple choice when possible
- YAGNI ruthlessly - remove unnecessary scope

**Discovery flow:**

1. **What are we building?**
   - "What do you want to add to the backlog?"
   - Let user describe freely

2. **Type identification**
   - What type of work is this?
   - `coding` - Software development, writing code
   - `docs` - Documentation, guides, technical writing
   - `ideation` - Brainstorming, exploring ideas
   - `general` - Research, planning, other tasks

3. **Scope clarification**
   - What's included?
   - What's explicitly NOT included?
   - Any constraints or dependencies?

4. **Success criteria**
   - How do we know when it's done?
   - What does "good" look like?

5. **Load type-specific guidelines**
   - Read `assets/{type}/guidelines.md`
   - Apply type-specific considerations

### Phase 3: Plan Mode

Enter Plan Mode to design the work structure.

**Feature number assignment:**
1. Read BACKLOG.md to find highest existing Feature number
2. New Feature = highest + 1 (e.g., if F3 exists, new one is F4)
3. If no features exist, start with F1

**Task sizing rule (CRITICAL):**
> Each Task must be completable in a **single Claude Code session**.
> If too big, break into smaller Tasks.
>
> Ask yourself: "Can an agent complete this without session reset?"
> - Yes → Good size
> - No → Break it down further

**Design the structure:**

```markdown
### F{n}: {Feature Name}
> {Brief description}

**Design**: [refs/designs/F{n}-{name}.md](refs/designs/F{n}-{name}.md)
**Context**: [active/F{n}-{name}.md](active/F{n}-{name}.md)

- [ ] T{n}.1: {Task name} `backlog`
  - [ ] T{n}.1.1: {Sub-task if needed}
- [ ] T{n}.2: {Task name} `backlog`
- [ ] T{n}.3: Review & Refactor F{n} `backlog`  ← verification/refactoring
```

> **Note**: Type, Goals, and detailed design information go in the Design doc, not BACKLOG.md.

**Review & Refactor tasks (REQUIRED):**

Task cycle: `ideation → plan → implement → verify/refactor → ... → done → final review/refactor`

| Situation | Task to add |
|-----------|-------------|
| End of every Feature | `Review & Refactor F{n}` - verify, improve, clean up |
| After complex Task (3+ sub-tasks) | `Review T{n}.Y` - intermediate check & improve |
| Integration points | `Review integration` - verify + refactor if needed |

**What Review & Refactor includes:**
- Verify functionality works as expected
- Check for bugs, edge cases
- Refactor messy code / improve structure
- Clean up unnecessary comments, dead code
- Ensure consistency with codebase patterns

Examples:
```markdown
- [ ] T1.1: Login API `backlog`
- [ ] T1.2: Signup API `backlog`
- [ ] T1.3: Review T1.1-T1.2 `backlog`      ← intermediate verification
- [ ] T1.4: Token refresh `backlog`
- [ ] T1.5: Review & Refactor F1 `backlog`  ← end-of-Feature review/refactor
```

**Present to user:**
- Show proposed structure
- Highlight task sizing
- **Show verification tasks** - explain why they're placed there
- Ask for approval or adjustments

### Phase 4: Add to Backlog

After user approval:

1. **Update BACKLOG.md**
   - Add new Feature section with Design and Context links
   - Task list only (no detailed information)
   - Maintain priority ordering (new items at bottom unless specified)

2. **Create Design doc** (`refs/designs/F{n}-{name}.md`)
   - Use FEATURE-DESIGN-TEMPLATE.md
   - Include Type (coding/docs/ideation/general)
   - Fill in Goals, Non-Goals, Design approach from brainstorming
   - Record any decisions made during brainstorming

3. **Create Active context** (`active/F{n}-{name}.md`)
   - Use ACTIVE-FEATURE-TEMPLATE.md
   - Set Phase to "design" or "implementation"
   - Link to Design doc in Related Files

4. **Confirm addition**
   ```
   Added to BACKLOG.md:
   - F{n}: {Feature Name}
     - T{n}.1: {Task}
     - T{n}.2: {Task}

   Created:
   - refs/designs/F{n}-{name}.md (design doc)
   - active/F{n}-{name}.md (working context)

   Ready to work? Start with: @INSTRUCTION.md #your-name
   ```

### Phase 5: Next Step (Optional)

After confirming addition, offer to detail-plan Tasks:

```
Would you like to detail-plan any of the new Tasks now?
1. Yes → Which Task? (runs /sprint:plan-backlog)
2. No → End skill
```

If user selects Yes:
- Ask which Task to plan
- Invoke `/sprint:plan-backlog` for the selected Task
- This breaks down the Task into Sub-tasks with detailed implementation plan

If user selects No:
- End the skill
- User can run `/sprint:plan-backlog` later when needed

---

## Task Sizing Guidelines

### Good Task Size (Single Session)
- Implement one API endpoint
- Write tests for one component
- Create one documentation page
- Fix one specific bug
- Add one UI component

### Too Big (Break Down)
- "Implement authentication system" → Break into: login API, signup API, token refresh, etc.
- "Write all API documentation" → Break into: one doc per endpoint group
- "Refactor the entire module" → Break into: one file or one pattern at a time

### Rule of Thumb
- Can describe what to do in 2-3 sentences? Good size.
- Need a paragraph to explain? Too big.
- "Just do X" where X is clear? Good size.
- "Do X, Y, Z, and handle A, B, C"? Too big.

---

## Assets

Type-specific guidelines:
- `assets/coding/guidelines.md` - For software development tasks
- `assets/docs/guidelines.md` - For documentation tasks
- `assets/ideation/guidelines.md` - For brainstorming/exploration tasks
- `assets/general/guidelines.md` - For general tasks
