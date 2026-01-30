# Work Board

> Real-time view of current work. Full backlog in BACKLOG.md.

---

## Before You Start (REQUIRED)

- [ ] Read `BACKLOG.md` - Find your assigned or available tasks
- [ ] Read `refs/decisions/F{n}-*.md` - If working on Feature n
- [ ] Check `active/F{n}-*.md` - Feature context (if exists)
- [ ] Check **Dependencies** below - Ensure nothing blocks your task

---

## WIP Limit: 1 task per agent

Each agent may only have **one task in_progress** at a time.

---

## Team

| Agent | Focus Area | Status |
|-------|-----------|--------|
| #danny | F1: Payment | Active |
| #agent-1 | F2: Order | Active |

---

## In Progress

| Feature | Task | Agent | Started | Notes |
|---------|------|-------|---------|-------|
| F1 | T1.2: Create Payment Intent | #danny | 2024-01-28 | Stripe API integration |
| F2 | T2.2: Create Order API | #agent-1 | 2024-01-28 | DB transaction handling |

---

## In Review

| Feature | Task | Agent | Reviewer | Notes |
|---------|------|-------|----------|-------|
| | | | | |

---

## Recently Done

> Last 5 items.

| Feature | Task | Agent | Completed | Notes |
|---------|------|-------|-----------|-------|
| F2 | T2.1: Order Model | #agent-1 | 2024-01-28 | With migration |
| F1 | T1.1: Stripe SDK | #danny | 2024-01-27 | Test mode configured |

---

## Dependencies

> Feature/Task dependencies. Check before starting work.

| Item | Depends On | Status | Notes |
|------|-----------|--------|-------|
| T2.4 | T1.3 | T1.3 backlog | Needs Webhook for refund |
| T3.2 | T2.2 | T2.2 in_progress | Email after order complete |
| T3.3 | T1.4 | T1.4 backlog | Receipt after payment |
| F3 | F1, F2 | Partially complete | Needs some F1, F2 complete |

---

## Blockers

| Task | Agent | Blocker | Since |
|------|-------|---------|-------|
| T2.4 | - | T1.3 incomplete (Webhook) | 2024-01-28 |
| T3.2 | - | T2.2 incomplete (Order API) | 2024-01-28 |
| T3.3 | - | T1.4 incomplete (Payment confirm) | 2024-01-28 |

---

## Coordination Notes

### #danny ↔ #agent-1 Collaboration Points

1. **T1.3 (Webhook) → T2.4 (Cancel Order)**
   - #danny notifies #agent-1 when T1.3 completes
   - Need prior agreement on refund logic interface

2. **T2.2 (Create Order) → T1.2 (Payment Intent)**
   - Payment integration after order creation
   - Order ID format agreed: UUID v4

---

## Quick Actions

### Claim a task
1. Find unclaimed task in BACKLOG.md (no #agent)
2. Add `#yourname`, change status to `in_progress`
3. Add entry to **In Progress** table
4. Check Dependencies - verify not blocked

### Complete a task
1. Move from **In Progress** to **Recently Done**
2. Update BACKLOG.md: mark `[x]`, status to `done`
3. **Check if this unblocks other tasks** - Update Dependencies
4. **END SESSION**

### Handle blocker
1. Add to **Blockers** table
2. Document blocking task
3. Do NOT claim new task
4. Coordinate with blocking agent if needed
