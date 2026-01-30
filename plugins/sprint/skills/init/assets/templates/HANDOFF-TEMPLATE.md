# Work Board

> Real-time view of current work. Full backlog in BACKLOG.md.

---

## Before You Start (REQUIRED)

- [ ] Read `BACKLOG.md` - Find your assigned or available tasks
- [ ] Read `refs/decisions/F{n}-*.md` - If working on Feature n (if exists)
- [ ] Read `refs/lessons/F{n}-*.md` - If working on Feature n (if exists)
- [ ] Check `active/F{n}-*.md` - Feature context (if exists)
- [ ] Check **Dependencies** below - Ensure nothing blocks your task

---

## WIP Limit: 1 task per agent

Each agent may only have **one task in_progress** at a time.
Complete or move to review before claiming another.

---

## In Progress

| Feature | Task | Agent | Started | Notes |
|---------|------|-------|---------|-------|
| | | | | |

<!-- Example:
| F1 | T1.2: Login API | #danny | 2024-01-28 | JWT implementation |
-->

---

## In Review

| Feature | Task | Agent | Reviewer | Notes |
|---------|------|-------|----------|-------|
| | | | | |

---

## Recently Done

> Last 5 items. Archive older to refs/changelog.md.

*None yet.*

---

## Dependencies

> Feature/Task dependencies. Check before starting work.

| Item | Depends On | Status | Notes |
|------|-----------|--------|-------|
| | | | |

<!-- Example:
| F2 | F1 | F1 in_progress | F2 blocked until F1 auth API done |
| T3.2 | T3.1 | T3.1 done | Can start T3.2 now |
-->

---

## Blockers

| Task | Agent | Blocker | Since |
|------|-------|---------|-------|
| | | | |

---

## Quick Actions

### Claim a task
1. Find unclaimed task in BACKLOG.md (no #agent)
2. Add `#yourname` to task in BACKLOG.md, change status to `in_progress`
3. Add entry to **In Progress** table above
4. Create `active/F{n}-name.md` if first task for that feature

### Complete a task
1. Move from **In Progress** to **Recently Done** (or **In Review**)
2. Update BACKLOG.md: mark with `[x]`, status to `done` or `review`
3. Update `active/F{n}-name.md` with completion notes
4. **END SESSION** - Do NOT claim next task automatically

> One session = One task. Start new session with `@INSTRUCTION.md` for next task.

### Handle blocker
1. Add to **Blockers** table above
2. Document in your In Progress notes
3. Do NOT claim new task (respect WIP limit)
4. Notify team lead if critical
