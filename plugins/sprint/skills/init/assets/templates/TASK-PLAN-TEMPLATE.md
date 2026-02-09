# F{n}/T{m}: {Task Name} Plan

> Execution plan for this task. Optional for simple tasks.
> **Self-contained**: This file must have all context needed after clear context.

---

## Sprint Context

| Key | Value |
|-----|-------|
| Sprint | `{sprint-path}` |
| Feature | `F{n}: {feature-name}` |
| Task | `T{m}: {task-name}` |
| Plan File | `{this-file-absolute-path}` |

**Required reads after clear context:**
1. `{sprint-path}/BACKLOG.md` - Task status, assignments
2. `{sprint-path}/HANDOFF.md` - Current work board
3. `{sprint-path}/refs/designs/F{n}-*.md` - Feature design (if exists)
4. `{sprint-path}/active/F{n}-*.md` - Feature working context (if exists)

---

## Task

What needs to be done (copy from BACKLOG.md).

## Approach

Step-by-step execution plan:

1. Step 1
2. Step 2
3. Step 3

---

## Sub-tasks

- [ ] Sub-task 1
- [ ] Sub-task 2
- [ ] Sub-task 3

---

## Agent Teams (if applicable)

> Remove this section if single-agent execution is sufficient.

**Purpose:** {speed | quality | both}

| Agent | Role | Sub-tasks |
|-------|------|-----------|
| lead | {role} | {sub-tasks} |
| worker-1 | {role} | {sub-tasks} |

**Dependencies:** {which sub-tasks block others}
**Merge point:** {when/how results are integrated}

---

## Files to Modify

| File | Change |
|------|--------|
| path/to/file1 | Add X |
| path/to/file2 | Modify Y |

---

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

---

## Risks / Considerations

- Risk 1: Mitigation
