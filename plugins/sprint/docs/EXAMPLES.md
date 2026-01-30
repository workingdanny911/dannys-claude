# Sprint Plugin - Real-World Examples

## Example 1: Web API Project

### Scenario

"I want to build a user management API. Need authentication, profile, and settings features."

### Step 1: Initialize Sprint

```
User: /sprint:init

Claude: What should we call this sprint? (kebab-case recommended)

User: user-management-api

Claude: Where should we create it?
1. sprints/user-management-api/ (default)
2. Custom path

User: 1

Claude: Sprint created.

sprints/user-management-api/
├── BACKLOG.md
├── HANDOFF.md
├── INSTRUCTION.md
├── .sprint-version
├── active/
└── refs/
    ├── designs/
    ├── plans/
    ├── decisions/
    │   └── _sprint.md
    ├── lessons/
    │   └── _sprint.md
    └── archive/

Next: Use /sprint:add-backlog to add work items.
```

### Step 2: Add Features

```
User: /sprint:add-backlog

Claude: What do you want to build?

User: Authentication feature - login, signup, password reset

Claude: What type of work is this?
1. coding (recommended)
2. docs
3. ideation
4. general

User: 1

Claude: Let's define the scope.

Include:
- Login
- Signup
- Password reset

Anything to exclude?

User: Social login for later

Claude: Success criteria?

User: APIs work and tests pass

Claude: [Entering Plan Mode]

Proposed structure:

### F1: Authentication
> User auth (login, signup, password reset)
> Social login excluded

**Type**: coding

- [ ] T1.1: Login API `backlog`
- [ ] T1.2: Signup API `backlog`
- [ ] T1.3: Password Reset API `backlog`
- [ ] T1.4: Auth Integration Tests `backlog`
- [ ] T1.5: Review & Refactor F1 `backlog`

Proceed?

User: Yes

Claude: Added to BACKLOG.md.

Create design doc? (2+ tasks → recommended)

User: Yes

Claude: Created refs/designs/F1-authentication.md
```

### Step 3: Work on Tasks

```
User: @sprints/user-management-api/INSTRUCTION.md #danny

Claude: Starting session as #danny.

[Loading context]

Current state:
- F1: Authentication (5 tasks)
  - T1.1: Login API `backlog` ← Top priority
  - T1.2: Signup API `backlog`
  - ...

Claiming and starting T1.1: Login API.

[Updating BACKLOG.md: T1.1 → #danny `in_progress`]
[Updating HANDOFF.md: Adding to In Progress]
[Creating active/F1-authentication.md]

[Entering Plan Mode - Login API implementation plan]

## Login API Implementation Plan

### T1.1.1: Define Schema
- POST /api/auth/login
- Request: { email, password }
- Response: { accessToken, refreshToken, user }

### T1.1.2: Implement Endpoint
- JWT token generation
- Password verification (bcrypt)

### T1.1.3: Add Validation
- Email format validation
- Password minimum requirements

Proceed with this plan?

User: Go ahead

[Implementation in progress...]

Claude: Completed T1.1: Login API.

Completed:
- POST /api/auth/login endpoint
- JWT token issuance logic
- bcrypt password verification
- Input validation

Updated files:
- src/routes/auth.ts
- src/services/auth.ts
- src/validators/auth.ts

Sprint file updates:
- BACKLOG.md: T1.1 → `done`
- HANDOFF.md: Moved to Recently Done
- active/F1-authentication.md: Progress recorded

Ending session. For next Task:
@sprints/user-management-api/INSTRUCTION.md #danny
```

### Step 4: Next Task

```
User: @sprints/user-management-api/INSTRUCTION.md #danny

Claude: Starting session as #danny.

[Loading context]

Current state:
- F1: Authentication
  - [x] T1.1: Login API `done`
  - T1.2: Signup API `backlog` ← Next
  - ...

Starting T1.2: Signup API.
```

---

## Example 2: Documentation Project

### Scenario

"I want to write documentation for existing APIs."

### Initialize Sprint

```
User: /sprint:init

Claude: Sprint name?

User: api-documentation

Claude: Created.
```

### Add Features

```
User: /sprint:add-backlog

Claude: What do you want to build?

User: API docs - auth, user, and order API documentation

Claude: Type?

User: 2 (docs)

Claude: [Plan Mode]

### F1: API Documentation
> Auth, User, Order API documentation

**Type**: docs

- [ ] T1.1: Auth API Documentation `backlog`
- [ ] T1.2: User API Documentation `backlog`
- [ ] T1.3: Order API Documentation `backlog`
- [ ] T1.4: Review & Refactor F1 `backlog`

User: Looks good

Claude: Added to BACKLOG.md.
```

### Work

```
User: @sprints/api-documentation/INSTRUCTION.md #danny

Claude: Starting T1.1: Auth API Documentation.

[Writing documentation...]

Created docs/api/authentication.md.

Ending session.
```

---

## Example 3: Multi-Agent Collaboration

### Scenario

Two Claude Code sessions working simultaneously

### Setup

```
# Session 1
User: @sprints/my-sprint/INSTRUCTION.md #danny

# Session 2 (different terminal)
User: @sprints/my-sprint/INSTRUCTION.md #agent-1
```

### BACKLOG.md State

```markdown
### F1: Authentication
- [ ] T1.1: Login API #danny `in_progress`
- [ ] T1.2: Signup API `backlog`

### F2: User Profile
- [ ] T2.1: Get Profile API #agent-1 `in_progress`
- [ ] T2.2: Update Profile API `backlog`
```

### HANDOFF.md State

```markdown
## In Progress

| Feature | Task | Agent | Started | Notes |
|---------|------|-------|---------|-------|
| F1 | T1.1: Login API | #danny | 2024-01-28 | JWT impl |
| F2 | T2.1: Get Profile API | #agent-1 | 2024-01-28 | Basic query |
```

### Conflict Prevention

```
# #danny modifies only F1 related
active/F1-authentication.md

# #agent-1 modifies only F2 related
active/F2-user-profile.md

# BACKLOG.md: each modifies only their assigned Task
# HANDOFF.md: each modifies only their row
```

---

## Example 4: Review and Improvement

### Review After Task Completion

```
User: /sprint:review-backlog T1.1

Claude: Starting review of T1.1: Login API.

Type: coding
Checklist: coding/checklist.md

### Review Results

### 🔴 Critical (1)
1. **SQL Injection vulnerability**
   - Location: src/services/auth.ts:45
   - Current: Direct string concatenation
   - Impact: Security vulnerability

### 🟡 Improvement (2)
1. **Insufficient error handling**
   - Current: All errors return 500
   - Suggestion: Use appropriate HTTP status codes

2. **Missing logging**
   - Suggestion: Log login attempts

### 🟢 Minor (1)
- Type definitions could improve

Create improvement plan?

User: Yes

Claude: [Plan Mode]

### Improvement Tasks

- [ ] T1.6: Fix review issues (T1.1) `backlog`
  - [ ] T1.6.1: Fix SQL injection vulnerability
  - [ ] T1.6.2: Improve error handling
  - [ ] T1.6.3: Add login attempt logging

Added to BACKLOG.md.
```

---

## Example 5: Breaking Down Complex Tasks

### Initial Addition

```
User: /sprint:add-backlog

Claude: What do you want to build?

User: Payment system

Claude: That's a broad scope. What specific features do you need?

User: Card payment, refunds, payment history

Claude: [Plan Mode]

### F3: Payment System
> Card payment, refunds, payment history

**Type**: coding

- [ ] T3.1: Payment Gateway Integration `backlog`
- [ ] T3.2: Process Payment API `backlog`
- [ ] T3.3: Refund API `backlog`
- [ ] T3.4: Payment History API `backlog`
- [ ] T3.5: Payment Integration Tests `backlog`
- [ ] T3.6: Review & Refactor F3 `backlog`

T3.1 looks complex. Want to design it in detail first?

User: Yes
```

### Detail Design with `/sprint:plan-backlog`

```
User: /sprint:plan-backlog T3.1

Claude: Starting design for T3.1: Payment Gateway Integration.

Which payment gateway?
1. Stripe (recommended) - Great docs, SDK provided
2. PayPal
3. Square
4. Other

User: 1

Claude: Payment methods?
1. Card only
2. Card + Bank transfer
3. All

User: 1

Claude: [Verifying understanding...]

[Plan Mode]

### T3.1: Payment Gateway Integration

- [ ] T3.1.1: Setup Stripe SDK
- [ ] T3.1.2: Create Payment Intent Wrapper
- [ ] T3.1.3: Webhook Handler Setup
- [ ] T3.1.4: Test with Stripe Test Mode

Updated BACKLOG.md.
Created refs/plans/F3-T1-payment-gateway.md.
```

---

## Example 6: Handling Blockers

### Blocker Occurs

```
User: @sprints/my-sprint/INSTRUCTION.md #danny

Claude: Starting T2.3: Notification API.

[Working...]

Issue found: T2.3 depends on T2.2 (User Preferences).
Need to read user notification settings, but T2.2 is not complete.

Marking T2.3 as blocked.

BACKLOG.md:
- [ ] T2.3: Notification API `blocked` → depends on T2.2

HANDOFF.md Blockers:
| T2.3 | #danny | T2.2 incomplete | 2024-01-28 |

Work on something else?
1. Start T2.2 first (recommended)
2. Pick Task from different Feature
3. End session

User: 1

Claude: Starting T2.2: User Preferences API.
```

### Blocker Resolved

```
Claude: Completed T2.2.

T2.3 blocker resolved.

BACKLOG.md:
- [ ] T2.3: Notification API `backlog` (unblocked)

Removed T2.3 from HANDOFF.md Blockers.

Ending session.
Start T2.3 in next session.
```

---

## Example 7: Sprint Version Update

### After Template Update

```
User: /sprint:update-version

Claude: Checking versions...

Current Sprint version: 1.0.0
Latest template version: 1.1.0

Update needed.

Changes:
- INSTRUCTION.md: Improved Context Recovery procedure
- BACKLOG.md: Updated Status diagram

Data to preserve:
- Features: 3
- Done: 2 records
- In Progress: 1 row

Proceed?

User: Yes

Claude: Backup created: refs/archive/_backup-v1.0.0/

Update complete!

Version: 1.0.0 → 1.1.0
All user data preserved.
```
