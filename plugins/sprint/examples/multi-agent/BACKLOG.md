# Backlog

> Single source of truth for all work items.
> Use `/sprint:add-backlog` to add new items.

---

## Legend

**Priority**: Top-to-bottom ordering. Items at top are highest priority.

**Urgent**: Prefix with `[URGENT]` to indicate time-sensitive items.

**Assignment**: `#agent-name` indicates who is working on it.

---

## Numbering

```
F{n}      - Feature number (F1, F2, F3...)
T{f}.{t}  - Task: Feature f, Task t (T1.1, T1.2, T2.1...)
T{f}.{t}.{s} - Sub-task (T1.1.1, T1.1.2...)
```

---

## Status & Transitions

```
backlog ──────► in_progress ──────► review ──────► done
                    │                  │
                    ▼                  │
                 blocked ◄─────────────┘
                    │
                    ▼
                 backlog (when unblocked)
```

---

## Features

### [URGENT] F1: Payment Integration
> Stripe payment integration (urgent - launch deadline)

**Design**: [refs/designs/F1-payment.md](refs/designs/F1-payment.md)
**Context**: [active/F1-payment.md](active/F1-payment.md)

- [x] T1.1: Stripe SDK Setup `done`
- [ ] T1.2: Create Payment Intent API #danny `in_progress`
- [ ] T1.3: Webhook Handler `backlog`
- [ ] T1.4: Payment Confirmation Flow `backlog`
- [ ] T1.5: Review & Refactor F1 `backlog`

---

### F2: Order Management
> Order creation, retrieval, cancellation

**Design**: [refs/designs/F2-order.md](refs/designs/F2-order.md)
**Context**: [active/F2-order.md](active/F2-order.md)

- [x] T2.1: Order Model & Migration `done`
- [ ] T2.2: Create Order API #agent-1 `in_progress`
- [ ] T2.3: Get Order API `backlog`
- [ ] T2.4: Cancel Order API `blocked` → depends on T1.3 (refund logic)
- [ ] T2.5: Review & Refactor F2 `backlog`

---

### F3: Notification System
> Email, push notifications

**Design**: [refs/designs/F3-notification.md](refs/designs/F3-notification.md)

- [ ] T3.1: Email Service Setup `backlog`
- [ ] T3.2: Order Confirmation Email `blocked` → depends on T2.2
- [ ] T3.3: Payment Receipt Email `blocked` → depends on T1.4
- [ ] T3.4: Review & Refactor F3 `backlog`

---

## Done

> Completed features. Keep last 3 summaries here.

*None yet.*

---

## Archiving

When a Feature is `done`:

1. Move full Feature section → `refs/archive/F{n}-name.md`
2. Leave one-line summary here:
   - `F1: Feature Name` - completed YYYY-MM-DD
