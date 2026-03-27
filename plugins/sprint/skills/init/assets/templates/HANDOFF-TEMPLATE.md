# Work Board

> Real-time view of current work. Full backlog in BACKLOG.md.

---

## Before You Start (REQUIRED)

- [ ] Check **Up Next** below - Pick highest priority task
- [ ] Read `active/F{n}-*.md` - Feature context (if exists)
- [ ] Check **Dependencies** below - Ensure nothing blocks your task

---

## Up Next

> Priority-ordered tasks ready to claim. Update when tasks complete or unblock.

| Priority | Task | Feature | Notes |
|----------|------|---------|-------|
| | | | |

<!-- Keep top 3-5 claimable tasks. Remove when claimed. -->

---

## In Progress

| Feature | Task | Persona | Started | Notes |
|---------|------|---------|---------|-------|
| | | | | |

<!-- Example:
| F1 | T1.2: Login API | #rook | 2024-01-28 | JWT implementation |
-->

---

## In Review

| Feature | Task | Persona | Reviewer | Notes |
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

| Task | Persona | Blocker | Since |
|------|-------|---------|-------|
| | | | |

---

## Quick Actions

### Claim a task
1. Find unclaimed task in BACKLOG.md (no #persona)
2. Add `#yourname` to task in BACKLOG.md, change status to `in_progress`
3. Add entry to **In Progress** table above
4. Create `active/F{n}-name.md` if first task for that feature

### Complete a task
1. Move from **In Progress** to **Recently Done** (or **In Review**)
2. Update BACKLOG.md: mark with `[x]`, status to `done` or `review`, remove `#persona`
   - **No detailed notes** - just checkbox and status change
3. Update **Up Next**: Add newly unblocked tasks with priority
4. Update `active/F{n}-name.md` with completion notes (details go here)
5. **END SESSION** - Do NOT claim next task automatically

> One session = One task. Start new session with `@INSTRUCTION.md #persona-name` for next task.

### Handle blocker
1. Add to **Blockers** table above
2. Document in your In Progress notes
3. Do NOT claim new task while blocked
4. Notify team lead if critical
