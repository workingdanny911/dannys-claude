---
name: briefing
description: "Explain work done on a Feature, Task, or topic using diagrams and storytelling. Two modes: Sprint-bound (Feature/Task ID within sprint) and General (git/code analysis). Triggers: 'briefing', 'explain', '브리핑해줘', '설명해줘'"
---

# Sprint Briefing Skill

Explain work done on a Feature, Task, or topic using diagrams and storytelling.

## When to Use

- Understand what happened on a Feature or Task
- Review progress before planning next steps
- Get a clear explanation of code structure and changes
- Prepare a saved document summarizing a body of work

---

## Step 1: Detect Mode & Identify Target

### Mode Detection

```
Sprint files exist (BACKLOG.md, HANDOFF.md)?
├── YES → Sprint-bound mode
└── NO  → General mode (git/code analysis)
```

### Target Identification

**User specifies target** → use it directly:

| Input | Action |
|-------|--------|
| `F{n}` | Feature-level briefing |
| `T{n}.{m}` | Task-level briefing |
| `F{n}, F{m}` | Feature group briefing |
| Module/path/topic | Code/git-based briefing |

**No target specified** → show available targets and ask. Do NOT assume.

---

## Step 2: Gather Information

> **CRITICAL: Read ALL sources BEFORE generating any explanation.**
> - Only state facts confirmed by sources
> - Mark inferences: "[inferred from commit message]"
> - Missing information → state honestly, never fabricate

### Sprint-bound Sources (read in order)

| Priority | Source | What to Read |
|----------|--------|-------------|
| 1. Always | Sprint status | `BACKLOG.md`, `HANDOFF.md` |
| 2. Target | Design & plans | `refs/designs/F{n}-*.md`, `refs/plans/F{n}-T{m}-*.md` |
| 3. Target | Working context | `active/F{n}-*.md` (contains decisions, progress, notes) |
| 4. Target | Archived context | `refs/archive/F{n}-*.md` (completed Features) |
| 5. Sprint-wide | Decisions & lessons | `refs/decisions/_sprint.md`, `refs/lessons/_sprint.md` |
| 6. Code | Git & source | `git log`, `git diff --stat`, source files, test files |
| 7. Related | Adjacent Features | Previous/next Features from BACKLOG.md ordering |

### General Mode Sources

| Source | Method |
|--------|--------|
| Git history | `git log --oneline -30 -- <path>`, `git log --stat -10 -- <path>` |
| Code structure | Glob/read directory, entry points, main modules |
| Documentation | README, docs if present |
| Tests | Test files for verified behavior |

### Fact Registry (internal, not shown to user)

Before generating, mentally verify you have: Status, Timeline, Decisions, Architecture, Remaining work, Risks/blockers, Gaps, Inferences (with source).

---

## Step 3: Generate Briefing

### Sections

| # | Section | When | Purpose |
|---|---------|------|---------|
| 1 | 🎯 **Overview** | Always | What + current status |
| 2 | 📍 **Where We Are** | Always | Big picture position (ASCII diagram) |
| 3 | 📖 **The Story So Far** | Always | Narrative with chapters |
| 4 | 🔍 **Key Changes** | Always | Files changed, patterns introduced |
| 5 | 🧩 **Code Map** | Code only | Unit relationships and roles |
| 6 | 🗺️ **What's Ahead** | Always | Remaining work, related Features |
| 7 | 💡 **Good to Know** | Always | Decisions, lessons, risks, open questions |
| 8 | 📋 **At a Glance** | Always | Summary table |

### Section Guidelines

**🎯 Overview** — One paragraph: what this is + where it stands.

**📍 Where We Are** — ASCII diagram showing position in sprint or architecture.
```
Sprint: payment-system
========================================
F1: User Auth .......... [####====--] 60%
F2: User Profile ....... [----------]  0%
========================================
                          ^ YOU ARE HERE
```
> ASCII diagrams: **ENGLISH ONLY** (Korean breaks alignment). Verify alignment is correct.

**📖 The Story So Far** — Narrative chapters per completed task. Past tense for done, present tense for in-progress. Reference decision sources.
```
**Chapter 1: Foundation (T1.1 — DB Schema)**
The journey started with designing the data model...

**Chapter 2: Now (T1.3 — Token Refresh)**
Currently implementing refresh token rotation...
```

**🔍 Key Changes** — Table of files changed + key patterns introduced.

**🧩 Code Map** — Unit relationship diagram + roles table. Omit for non-code briefings.

**🗺️ What's Ahead** — Remaining tasks + related Features (previous/next with connections).

**💡 Good to Know** — Decisions (with source), lessons, open questions, risks. If none recorded, say so honestly.

**📋 At a Glance** — Key-value summary table (target, status, tasks, key files, decisions count, blockers, next up).

### Depth Rules (automatic, do NOT ask user)

| Target | Depth |
|--------|-------|
| Feature (many tasks) | Full — each task gets a chapter |
| Feature (few tasks) | Concise — combine small tasks |
| Single Task | Focused — that task's journey |
| Feature Group | Comparative — each summarized, connections highlighted |
| General (module) | Git-driven |

### Missing Information

Never skip a section silently. Show it with explanation:
```
Key Decisions:
No decision records found for F2.
[inferred from commit abc123] Chose REST over GraphQL based on commit message.
```

---

## Step 4: Save (Optional)

After displaying the briefing, ask if user wants to save.

**If yes:**
1. Suggest location: `refs/briefings/F{n}-briefing-YYYY-MM-DD.md` (sprint) or ask user (general)
2. Convert ASCII diagrams → Mermaid for the saved document
3. Add metadata header (Generated date, Target, Mode, Sprint) and Sources footer

**ASCII → Mermaid mapping:**

| ASCII | Mermaid |
|-------|---------|
| Sprint progress bar | `gantt` |
| Architecture box diagram | `flowchart LR` |
| Unit dependency map | `flowchart TD` |
| Request/sequence flow | `sequenceDiagram` |

---

## Key Principles

- **Accuracy > creativity** — Every fact traces to a source. Mark inferences. Never fabricate.
- **Read-only** — Does NOT modify sprint files. Only reads and optionally saves briefing.
- **Story-driven** — Tell the story of the work, not just list facts.
- **Diagrams in English** — ASCII uses English only. Verify monospace alignment.
- **User controls save** — Never auto-save. Always ask.
- **Automatic depth** — Skill decides detail level based on scope.
- **Show gaps honestly** — Missing info stated clearly, never filled with assumptions.

---

## Related Skills

- `/sprint:review-backlog` — Comprehensive quality review (audit-oriented)
- `/sprint:review-work` — Same-session review and done-marking (action-oriented)
- `/sprint:plan-backlog` — Design and break down work items (planning-oriented)
- `/sprint:add-backlog` — Add new backlog items
- `@INSTRUCTION.md` — Start work sessions
